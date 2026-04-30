import os
import shutil
from pathlib import Path

os.environ["SUPABASE_ENABLED"] = "0"
os.environ["SECRET_KEY"] = "test-secret"

import app as stundeneingabe_app


def test_healthcheck_responds_ok():
    client = stundeneingabe_app.app.test_client()

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json["ok"] is True
    assert response.json["service"] == "stundeneingabe-next-gen"


def test_validate_timesheet_day_rejects_invalid_project_number():
    day, errors = stundeneingabe_app.validate_timesheet_day({
        "workDate": "2026-04-30",
        "employeeCode": "nw",
        "startTime": "07:00",
        "endTime": "08:00",
        "breakMinutes": 0,
        "entries": [{
            "projectNumber": "26VG01",
            "hours": "1",
            "costCenter": "IWS",
        }],
    })

    assert day is None
    assert any("Vorgangsnr" in error for error in errors)


def test_create_day_writes_local_prototype_file(monkeypatch):
    test_dir = Path(__file__).resolve().parent / "_tmp_state"
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir(parents=True)
    monkeypatch.setattr(stundeneingabe_app, "DATA_DIR", test_dir)
    monkeypatch.setattr(stundeneingabe_app, "LOCAL_DAYS_FILE", test_dir / "timesheet_days.local.json")
    client = stundeneingabe_app.app.test_client()

    response = client.post("/api/days", json={
        "workDate": "2026-04-30",
        "employeeCode": "nw",
        "startTime": "07:00",
        "endTime": "08:00",
        "breakMinutes": 0,
        "entries": [{
            "customerName": "RS",
            "projectNumber": "26VG0001",
            "costCenter": "IWS",
            "hours": "1",
            "activity": "Test",
        }],
    })

    assert response.status_code == 201
    assert response.json["ok"] is True
    assert (test_dir / "timesheet_days.local.json").exists()


def test_assign_workflow_moves_submitted_day_to_assigned(monkeypatch):
    test_dir = Path(__file__).resolve().parent / "_tmp_state_workflow"
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir(parents=True)
    monkeypatch.setattr(stundeneingabe_app, "DATA_DIR", test_dir)
    monkeypatch.setattr(stundeneingabe_app, "LOCAL_DAYS_FILE", test_dir / "timesheet_days.local.json")
    client = stundeneingabe_app.app.test_client()

    create_response = client.post("/api/days", json={
        "workDate": "2026-04-30",
        "employeeCode": "nw",
        "startTime": "07:00",
        "endTime": "08:00",
        "breakMinutes": 0,
        "status": "submitted",
        "entries": [{
            "projectNumber": "26VG0001",
            "costCenter": "IWS",
            "hours": "1",
        }],
    })
    day_id = create_response.json["day"]["id"]

    response = client.post(f"/api/days/{day_id}/workflow", json={
        "action": "assign",
        "reviewer": "nilsw",
        "actor": "test",
    })

    assert response.status_code == 200
    assert response.json["day"]["status"] == "assigned"
    assert response.json["day"]["assignedTo"] == "nilsw"
    assert response.json["day"]["workflowEvents"][-1]["action"] == "assign"


def test_done_requires_office_entered_status():
    day = {"status": "approved", "workflowEvents": []}

    updated, errors = stundeneingabe_app.apply_workflow_action(day, {"action": "done"})

    assert updated is None
    assert any("eingegebene" in error for error in errors)
