from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request, send_from_directory


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOCAL_DAYS_FILE = DATA_DIR / "timesheet_days.local.json"

ROLES = ["employee", "assigner", "reviewer", "office", "admin"]
STATUSES = [
    "draft",
    "submitted",
    "assigned",
    "change_requested",
    "approved",
    "office_entered",
    "done",
    "cancelled",
]
REVIEWERS = [
    {"id": "nilsr", "label": "Nils R"},
    {"id": "nilsw", "label": "Nils W"},
    {"id": "matthias", "label": "Matthias"},
]
STATUS_LABELS = {
    "draft": "Entwurf",
    "submitted": "Eingereicht",
    "assigned": "Zugewiesen",
    "change_requested": "Aenderung angefordert",
    "approved": "Freigegeben",
    "office_entered": "Rike/Buero eingegeben",
    "done": "Fertig",
    "cancelled": "Verworfen",
}


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_dotenv(BASE_DIR / ".env")

SUPABASE_ENABLED = os.getenv("SUPABASE_ENABLED", "0").strip() == "1"
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip().rstrip("/")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me").strip() or "dev-only-change-me"

app = Flask(__name__, static_folder=None)
app.secret_key = SECRET_KEY


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def supabase_configured() -> bool:
    return bool(SUPABASE_ENABLED and SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY)


def read_local_days() -> list[dict[str, Any]]:
    if not LOCAL_DAYS_FILE.exists():
        return []
    try:
        payload = json.loads(LOCAL_DAYS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return payload if isinstance(payload, list) else []


def write_local_days(days: list[dict[str, Any]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    temp_path = LOCAL_DAYS_FILE.with_suffix(".tmp")
    temp_path.write_text(json.dumps(days, ensure_ascii=False, indent=2), encoding="utf-8")
    temp_path.replace(LOCAL_DAYS_FILE)


def sort_days(days: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        days,
        key=lambda day: (
            str(day.get("workDate") or ""),
            str(day.get("employeeCode") or ""),
            str(day.get("createdAt") or ""),
        ),
        reverse=True,
    )


def normalize_employee_code(value: Any) -> str:
    return " ".join(str(value or "").strip().upper().split())


def parse_number(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value or "").strip().replace(",", ".")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_time_to_minutes(value: Any) -> int | None:
    match = re.match(r"^(\d{1,2}):(\d{2})$", str(value or "").strip())
    if not match:
        return None
    hour = int(match.group(1))
    minute = int(match.group(2))
    if hour > 23 or minute > 59:
        return None
    return hour * 60 + minute


def calc_expected_hours(start_time: Any, end_time: Any, break_minutes: int) -> float | None:
    start = parse_time_to_minutes(start_time)
    end = parse_time_to_minutes(end_time)
    if start is None or end is None or break_minutes < 0:
        return None
    net_minutes = end - start - break_minutes
    if net_minutes < 0:
        return None
    return net_minutes / 60


def is_valid_project_number(value: Any) -> bool:
    text = str(value or "").strip().upper()
    if text in {"", "-"}:
        return True
    return bool(re.match(r"^\d{2}VG0\d{3}$", text))


def normalize_project_number(value: Any) -> str:
    text = str(value or "").strip().upper()
    if not text or text == "-" or re.match(r"^\d{2}VG0$", text):
        return ""
    return text


def validate_timesheet_day(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    work_date = str(payload.get("workDate") or payload.get("work_date") or "").strip()
    employee_code = normalize_employee_code(payload.get("employeeCode") or payload.get("employee_code"))
    start_time = str(payload.get("startTime") or payload.get("start_time") or "").strip()
    end_time = str(payload.get("endTime") or payload.get("end_time") or "").strip()
    break_raw = payload.get("breakMinutes", payload.get("break_minutes", 0))

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", work_date):
        errors.append("Datum ist Pflicht und muss YYYY-MM-DD sein.")
    if not employee_code:
        errors.append("Mitarbeiterkuerzel ist Pflicht.")

    try:
        break_minutes = int(str(break_raw).strip() or "0")
    except ValueError:
        break_minutes = -1
    if break_minutes < 0:
        errors.append("Pause muss eine ganze Minutenzahl >= 0 sein.")

    expected_hours = None
    if start_time or end_time:
        expected_hours = calc_expected_hours(start_time, end_time, break_minutes)
        if expected_hours is None:
            errors.append("Anfangszeit, Endzeit und Pause sind nicht plausibel.")

    entries_payload = payload.get("entries")
    if not isinstance(entries_payload, list) or not entries_payload:
        errors.append("Mindestens eine Stundenzeile ist erforderlich.")
        entries_payload = []

    entries: list[dict[str, Any]] = []
    total_hours = 0.0
    for index, row in enumerate(entries_payload, start=1):
        if not isinstance(row, dict):
            errors.append(f"Zeile {index}: ungueltiges Format.")
            continue
        hours = parse_number(row.get("hours"))
        if hours is None or hours <= 0:
            errors.append(f"Zeile {index}: Stunden muessen > 0 sein.")
            hours = 0.0
        project_number = normalize_project_number(row.get("projectNumber") or row.get("project_number"))
        if not is_valid_project_number(project_number):
            errors.append(f"Zeile {index}: Vorgangsnr. muss Format YYVG0NNN haben.")
        cost_center = str(row.get("costCenter") or row.get("cost_center") or "").strip().upper()
        if cost_center and cost_center != "-" and not re.match(r"^[A-Z]{3}$", cost_center):
            errors.append(f"Zeile {index}: Kostenstelle muss ein dreistelliger Code sein.")
        total_hours += hours
        entries.append({
            "id": str(row.get("id") or uuid.uuid4()),
            "customerName": str(row.get("customerName") or row.get("customer_name") or "").strip(),
            "projectNumber": project_number,
            "costCenter": "" if cost_center == "-" else cost_center,
            "isByEffort": bool(row.get("isByEffort") or row.get("is_by_effort")),
            "hours": round(hours, 2),
            "activity": str(row.get("activity") or "").strip(),
            "sortOrder": index * 10,
        })

    if expected_hours is not None and abs(total_hours - expected_hours) > 0.01:
        errors.append("Summe der Zeilenstunden passt nicht zu Anfang, Ende und Pause.")

    if errors:
        return None, errors

    now = utc_now_iso()
    normalized = {
        "id": str(payload.get("id") or uuid.uuid4()),
        "employeeCode": employee_code,
        "workDate": work_date,
        "startTime": start_time,
        "endTime": end_time,
        "breakMinutes": break_minutes,
        "controlHours": round(expected_hours, 2) if expected_hours is not None else None,
        "totalHours": round(total_hours, 2),
        "status": str(payload.get("status") or "draft"),
        "assignedTo": str(payload.get("assignedTo") or payload.get("assigned_to") or "").strip().lower(),
        "source": "local-prototype",
        "entries": entries,
        "workflowEvents": payload.get("workflowEvents") if isinstance(payload.get("workflowEvents"), list) else [],
        "createdAt": str(payload.get("createdAt") or now),
        "updatedAt": now,
    }
    if normalized["status"] not in STATUSES:
        normalized["status"] = "draft"
    if normalized["assignedTo"] and normalized["assignedTo"] not in {item["id"] for item in REVIEWERS}:
        normalized["assignedTo"] = ""
    return normalized, []


def get_day_or_error(day_id: str) -> tuple[list[dict[str, Any]], dict[str, Any] | None, Any | None]:
    days = read_local_days()
    for day in days:
        if str(day.get("id")) == day_id:
            return days, day, None
    return days, None, (jsonify({"ok": False, "error": "Tag nicht gefunden."}), 404)


def append_workflow_event(
    day: dict[str, Any],
    action: str,
    from_status: str,
    to_status: str,
    actor: str,
    note: str,
) -> None:
    events = day.get("workflowEvents")
    if not isinstance(events, list):
        events = []
        day["workflowEvents"] = events
    events.append({
        "id": str(uuid.uuid4()),
        "action": action,
        "fromStatus": from_status,
        "toStatus": to_status,
        "actor": actor,
        "note": note,
        "createdAt": utc_now_iso(),
    })


def apply_workflow_action(day: dict[str, Any], payload: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    action = str(payload.get("action") or "").strip().lower()
    actor = str(payload.get("actor") or "local-prototype").strip() or "local-prototype"
    note = str(payload.get("note") or "").strip()
    reviewer = str(payload.get("reviewer") or "").strip().lower()
    old_status = str(day.get("status") or "draft")
    errors: list[str] = []

    if action == "submit":
        if old_status not in {"draft", "change_requested"}:
            errors.append("Nur Entwurf oder Aenderungsanforderung kann eingereicht werden.")
        else:
            day["status"] = "submitted"
            day["assignedTo"] = ""
    elif action == "assign":
        reviewer_ids = {item["id"] for item in REVIEWERS}
        if reviewer not in reviewer_ids:
            errors.append("Bitte einen gueltigen Pruefer waehlen.")
        elif old_status not in {"submitted", "assigned"}:
            errors.append("Nur eingereichte Tage koennen zugewiesen werden.")
        else:
            day["status"] = "assigned"
            day["assignedTo"] = reviewer
    elif action == "approve":
        if old_status != "assigned":
            errors.append("Nur zugewiesene Tage koennen freigegeben werden.")
        else:
            day["status"] = "approved"
    elif action == "request_change":
        if old_status != "assigned":
            errors.append("Nur zugewiesene Tage koennen zur Aenderung markiert werden.")
        else:
            day["status"] = "change_requested"
    elif action == "office_entered":
        if old_status != "approved":
            errors.append("Nur freigegebene Tage koennen als eingegeben markiert werden.")
        else:
            day["status"] = "office_entered"
    elif action == "done":
        if old_status != "office_entered":
            errors.append("Nur eingegebene Tage koennen fertig gemeldet werden.")
        else:
            day["status"] = "done"
    elif action == "back_to_assigner":
        if old_status not in {"assigned", "change_requested", "approved"}:
            errors.append("Dieser Tag kann nicht an den Zuweiser zurueckgegeben werden.")
        else:
            day["status"] = "submitted"
            day["assignedTo"] = ""
    elif action == "back_to_office":
        if old_status != "done":
            errors.append("Nur fertige Tage koennen an Rike/Buero zurueckgestellt werden.")
        else:
            day["status"] = "office_entered"
    else:
        errors.append("Unbekannte Workflow-Aktion.")

    if errors:
        return None, errors

    new_status = str(day.get("status") or old_status)
    if action in {"approve", "request_change", "office_entered", "done"}:
        day[f"{new_status}At"] = utc_now_iso()
    day["updatedAt"] = utc_now_iso()
    append_workflow_event(day, action, old_status, new_status, actor, note)
    return day, []


@app.get("/")
def index() -> Any:
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/api/health")
def health() -> Any:
    return jsonify({
        "ok": True,
        "service": "stundeneingabe-next-gen",
        "savedAtUtc": utc_now_iso(),
        "supabaseConfigured": supabase_configured(),
    })


@app.get("/api/config")
def config() -> Any:
    return jsonify({
        "ok": True,
        "roles": ROLES,
        "statuses": STATUSES,
        "statusLabels": STATUS_LABELS,
        "reviewers": REVIEWERS,
        "storage": "supabase" if supabase_configured() else "local-prototype",
    })


@app.get("/api/days")
def get_days() -> Any:
    if supabase_configured():
        return jsonify({
            "ok": False,
            "error": "Supabase access is planned but not implemented in the prototype.",
        }), 501
    return jsonify({"ok": True, "days": sort_days(read_local_days())})


@app.post("/api/days")
def create_day() -> Any:
    if supabase_configured():
        return jsonify({
            "ok": False,
            "error": "Supabase write is planned but not implemented in the prototype.",
        }), 501
    payload = request.get_json(silent=True) or {}
    day, errors = validate_timesheet_day(payload)
    if errors or day is None:
        return jsonify({"ok": False, "errors": errors}), 400
    days = [existing for existing in read_local_days() if existing.get("id") != day["id"]]
    days.append(day)
    write_local_days(days)
    return jsonify({"ok": True, "day": day}), 201


@app.post("/api/days/<day_id>/workflow")
def update_day_workflow(day_id: str) -> Any:
    if supabase_configured():
        return jsonify({
            "ok": False,
            "error": "Supabase workflow is planned but not implemented in the prototype.",
        }), 501
    days, day, error_response = get_day_or_error(day_id)
    if error_response:
        return error_response
    payload = request.get_json(silent=True) or {}
    updated_day, errors = apply_workflow_action(day or {}, payload)
    if errors or updated_day is None:
        return jsonify({"ok": False, "errors": errors}), 400
    write_local_days(days)
    return jsonify({"ok": True, "day": updated_day})


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1").strip() or "127.0.0.1"
    port = int(os.getenv("PORT", "5056"))
    app.run(host=host, port=port, debug=False)
