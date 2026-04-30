-- Stundeneingabe Next Gen Supabase schema reference.
--
-- Status: Entwurf, noch nicht als echte Migration ausgefuehrt.
-- Vor Anwendung braucht es Zustimmung von Nils und ein bestaetigtes Supabase-Projekt.

create extension if not exists pgcrypto;

do $$
begin
  if not exists (select 1 from pg_type where typname = 'stundeneingabe_role') then
    create type public.stundeneingabe_role as enum (
      'employee',
      'assigner',
      'reviewer',
      'office',
      'admin'
    );
  end if;

  if not exists (select 1 from pg_type where typname = 'timesheet_status') then
    create type public.timesheet_status as enum (
      'draft',
      'submitted',
      'assigned',
      'change_requested',
      'approved',
      'office_entered',
      'done',
      'cancelled'
    );
  end if;
end $$;

create table if not exists public.employees (
  id uuid primary key default gen_random_uuid(),
  employee_code text not null unique,
  display_name text not null,
  is_active boolean not null default true,
  app_access_allowed boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint employees_code_format check (employee_code = upper(employee_code))
);

create table if not exists public.app_users (
  id uuid primary key default gen_random_uuid(),
  username text not null unique,
  display_name text not null,
  role public.stundeneingabe_role not null,
  employee_id uuid references public.employees(id) on delete set null,
  password_hash text not null,
  app_access_allowed boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.cost_centers (
  code text primary key,
  area text,
  button_label text,
  description text,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint cost_centers_code_format check (code ~ '^[A-Z]{3}$')
);

create table if not exists public.cost_center_templates (
  id uuid primary key default gen_random_uuid(),
  label text not null,
  customer_name text,
  project_prefix text,
  project_suffix text,
  cost_center_code text references public.cost_centers(code) on delete set null,
  is_by_effort boolean not null default false,
  activity text,
  start_time time,
  end_time time,
  break_minutes integer,
  hours numeric(6,2),
  display_order integer not null default 0,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint cost_center_templates_break_nonnegative check (break_minutes is null or break_minutes >= 0),
  constraint cost_center_templates_hours_positive check (hours is null or hours > 0),
  constraint cost_center_templates_project_suffix_format check (project_suffix is null or project_suffix ~ '^[0-9]{1,3}$')
);

create table if not exists public.timesheet_days (
  id uuid primary key default gen_random_uuid(),
  employee_id uuid not null references public.employees(id) on delete restrict,
  work_date date not null,
  start_time time,
  end_time time,
  break_minutes integer not null default 0,
  control_hours numeric(6,2),
  status public.timesheet_status not null default 'draft',
  assigned_to_user_id uuid references public.app_users(id) on delete set null,
  submitted_at timestamptz,
  approved_at timestamptz,
  office_entered_at timestamptz,
  done_at timestamptz,
  legacy_subject text,
  legacy_message_id text,
  source text not null default 'next-gen',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint timesheet_days_break_nonnegative check (break_minutes >= 0),
  constraint timesheet_days_unique_employee_date unique (employee_id, work_date, source)
);

create table if not exists public.time_entries (
  id uuid primary key default gen_random_uuid(),
  timesheet_day_id uuid not null references public.timesheet_days(id) on delete cascade,
  customer_name text,
  project_number text,
  cost_center_code text references public.cost_centers(code) on delete set null,
  is_by_effort boolean not null default false,
  hours numeric(6,2) not null,
  activity text,
  sort_order integer not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint time_entries_hours_positive check (hours > 0),
  constraint time_entries_project_format check (
    project_number is null
    or project_number = ''
    or project_number = '-'
    or project_number ~ '^[0-9]{2}VG0[0-9]{3}$'
  )
);

create table if not exists public.workflow_events (
  id uuid primary key default gen_random_uuid(),
  timesheet_day_id uuid not null references public.timesheet_days(id) on delete cascade,
  event_type text not null,
  from_status public.timesheet_status,
  to_status public.timesheet_status,
  actor_user_id uuid references public.app_users(id) on delete set null,
  note text,
  created_at timestamptz not null default now()
);

create table if not exists public.legacy_mail_imports (
  id uuid primary key default gen_random_uuid(),
  subject text not null,
  message_id text,
  mail_date timestamptz,
  body_hash text not null,
  app_version text,
  viewer_parse_warnings text,
  import_status text not null default 'pending',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (body_hash)
);

create index if not exists timesheet_days_work_date_idx on public.timesheet_days(work_date);
create index if not exists timesheet_days_status_idx on public.timesheet_days(status);
create index if not exists timesheet_days_assigned_to_idx on public.timesheet_days(assigned_to_user_id);
create index if not exists time_entries_day_idx on public.time_entries(timesheet_day_id, sort_order);
create index if not exists workflow_events_day_idx on public.workflow_events(timesheet_day_id, created_at);

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists employees_set_updated_at on public.employees;
create trigger employees_set_updated_at
before update on public.employees
for each row execute function public.set_updated_at();

drop trigger if exists app_users_set_updated_at on public.app_users;
create trigger app_users_set_updated_at
before update on public.app_users
for each row execute function public.set_updated_at();

drop trigger if exists cost_centers_set_updated_at on public.cost_centers;
create trigger cost_centers_set_updated_at
before update on public.cost_centers
for each row execute function public.set_updated_at();

drop trigger if exists cost_center_templates_set_updated_at on public.cost_center_templates;
create trigger cost_center_templates_set_updated_at
before update on public.cost_center_templates
for each row execute function public.set_updated_at();

drop trigger if exists timesheet_days_set_updated_at on public.timesheet_days;
create trigger timesheet_days_set_updated_at
before update on public.timesheet_days
for each row execute function public.set_updated_at();

drop trigger if exists time_entries_set_updated_at on public.time_entries;
create trigger time_entries_set_updated_at
before update on public.time_entries
for each row execute function public.set_updated_at();

alter table public.employees enable row level security;
alter table public.app_users enable row level security;
alter table public.cost_centers enable row level security;
alter table public.cost_center_templates enable row level security;
alter table public.timesheet_days enable row level security;
alter table public.time_entries enable row level security;
alter table public.workflow_events enable row level security;
alter table public.legacy_mail_imports enable row level security;
