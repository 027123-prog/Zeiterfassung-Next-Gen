# Datenbankschema

Zielanbieter ist Supabase/Postgres, analog Plantafel. Es wurde noch keine echte Migration ausgefuehrt.

## Grundregel

Strukturaenderungen werden nicht nur im Supabase-Dashboard vorgenommen. Jede Aenderung wird als SQL oder Doku festgehalten. `supabase/schema.sql` ist aktuell eine Schema-Referenz und noch keine angewendete Produktionsmigration.

## Tabellen

### `employees`

Mitarbeiter-Stammdaten und Kuerzel.

Wichtige Felder:

- `id`: UUID.
- `employee_code`: Kuerzel aus First Try, eindeutig.
- `display_name`: Anzeigename.
- `is_active`: Mitarbeiter ist aktiv.
- `app_access_allowed`: Login/Online-Erfassung erlaubt.

### `app_users`

Interne Benutzer fuer Login und Rollen.

Rollen:

- `employee`
- `assigner`
- `reviewer`
- `office`
- `admin`

Passwoerter werden nur gehasht gespeichert. Die Flask-App nutzt den Service Role Key serverseitig.

### `cost_centers`

Kostenstellenkatalog.

Wichtige Felder:

- `code`: dreistelliger Code, z. B. `FWS`, `SIU`, `ORD`.
- `area`: Bereich, z. B. Fussboden, Bauelemente, Buero.
- `button_label`: kurzer Buttontext.
- `description`: Beschreibung.
- `is_active`: weiter nutzbar.

### `cost_center_templates`

Vorlagen aus der bisherigen Excel-/CSV-Logik.

Wichtige Felder:

- `label`: Buttonname.
- `customer_name`
- `project_prefix`
- `project_suffix`
- `cost_center_code`
- `is_by_effort`
- `activity`
- `start_time`, `end_time`, `break_minutes`, `hours`

### `timesheet_days`

Ein eingereichter oder bearbeiteter Arbeitstag.

Wichtige Felder:

- `employee_id`
- `work_date`
- `start_time`
- `end_time`
- `break_minutes`
- `control_hours`
- `status`
- `assigned_to_user_id`
- `submitted_at`, `approved_at`, `office_entered_at`, `done_at`
- `legacy_subject`, `legacy_message_id`, `source`

Statuswerte:

- `draft`
- `submitted`
- `assigned`
- `change_requested`
- `approved`
- `office_entered`
- `done`
- `cancelled`

### `time_entries`

Stundenzeilen eines Tages.

Wichtige Felder:

- `timesheet_day_id`
- `customer_name`
- `project_number`
- `cost_center_code`
- `is_by_effort`
- `hours`
- `activity`
- `sort_order`

### `workflow_events`

Audit-Trail fuer Zuweisung, Freigabe, Aenderungsanforderung, Rike/Buero und Abschluss.

Wichtige Felder:

- `timesheet_day_id`
- `event_type`
- `from_status`
- `to_status`
- `actor_user_id`
- `note`
- `created_at`

### `legacy_mail_imports`

Optionaler Uebergangsspeicher fuer First-Try-Mails.

Wichtige Felder:

- `subject`
- `message_id`
- `mail_date`
- `body_hash`
- `app_version`
- `viewer_parse_warnings`
- `import_status`

## Validierungsregeln

- Datum ist Pflicht.
- Mitarbeiterkuerzel ist Pflicht und wird normalisiert.
- Vorgangsnummer ist leer erlaubt; wenn vorhanden, Format `YYVG0NNN`.
- Pause ist ganze Minutenzahl >= 0.
- Stunden pro Zeile > 0.
- Wenn Startzeit und Endzeit gesetzt sind, muss `Ende - Start - Pause` >= 0 sein.
- Tages-Sollstunden aus Zeiten/Pause muessen mit Zeilensumme innerhalb einer kleinen Toleranz uebereinstimmen, bevor ein Tag eingereicht wird.
- Kostenstelle ist ein dreistelliger Code oder bewusst leer/Platzhalter in Uebergangsdaten.

## Offene Entscheidungen

- Ob RLS ueber Flask-Service-Role hinaus spaeter fuer direkte Clientzugriffe genutzt wird.
- Ob alte `.eml`-Mails importiert werden oder nur als Archiv bleiben.
- Welche Benutzer und Rollen initial angelegt werden.
