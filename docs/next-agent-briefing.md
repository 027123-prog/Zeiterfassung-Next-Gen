# Briefing fuer die naechsten Agenten

Stand: 2026-04-30.

## Erst lesen

1. `AGENTS.md`
2. `context.md`
3. `tasks.md`
4. `PROJEKTDOKUMENTATION.md`
5. `docs/workflow.md`
6. `docs/db-schema.md`
7. `docs/architecture.md`
8. `docs/bestandsanalyse-first-try.md`
9. `legacy-reference/README.md`

## Wichtigste Leitplanken

- `Stundeneingabe First Try` bleibt stabil. Nicht im alten Projekt umbauen.
- `legacy-reference/` enthaelt nur Referenzkopien. Dort nichts als neue Produktivquelle weiterentwickeln.
- Keine echten Betriebsdaten, Mail-Exporte, `.env`, Passwoerter, Service Keys oder personenbezogene Excel-Listen ins Repo.
- Keine echte Supabase-Migration und kein Deployment ohne ausdrueckliche Freigabe von Nils.
- Bei Projektarbeit immer `PROJEKTDOKUMENTATION.md` und `tasks.md` aktualisieren.
- Vor Push mindestens `python -m py_compile app.py` und `python -m pytest` ausfuehren.

## Aktueller technischer Stand

- Flask-Prototyp in `app.py`.
- Frontend in `index.html`.
- Lokale Demo-Daten landen in `data/timesheet_days.local.json` und sind ignoriert.
- API:
  - `GET /api/health`
  - `GET /api/config`
  - `GET /api/days`
  - `POST /api/days`
  - `POST /api/days/<id>/workflow`
- Tests in `tests/test_app.py`.
- Supabase-Schema nur als Entwurf in `supabase/schema.sql`.
- Legacy-Dateien aus First Try liegen als Referenz unter `legacy-reference/first-try/`, ohne Excel-Datei.

## Naechste sinnvolle Schritte

### 1. Oberflaeche naeher an First Try ziehen

Ziel:

- Mitarbeiteransicht soll wieder wie die gewohnte mobile Stundeneingabe wirken.
- Buero-/Pruefansicht soll fachlich naeher am alten Viewer liegen.
- Der bestehende technische Prototyp darf als Backend-Grundlage bleiben.

Akzeptanzkriterien:

- Mitarbeiter kann einen Tag mit den bekannten Feldern erfassen.
- Die Ansicht ist mobil gut nutzbar.
- Status-/Workflowliste bleibt nutzbar.
- Kein Bruch der bestehenden Tests.

### 2. Mehrere Stundenzeilen pro Tag

Ziel:

- Ein Tag kann mehrere Zeilen enthalten, wie in First Try.

Akzeptanzkriterien:

- Zeilen koennen hinzugefuegt und entfernt werden.
- Tagesstunden werden summiert.
- Soll/Ist-Pruefung aus Anfang, Ende und Pause bleibt erhalten.
- API-Validierung akzeptiert mehrere Zeilen und lehnt ungueltige Zeilen sauber ab.

### 3. Kostenstellenkatalog und Vorlagenpflege

Ziel:

- Kostenstellen und Vorlagen sollen nicht mehr ueber Excel gepflegt werden.
- Admin/Buero soll Vorlagen spaeter in der Weboberflaeche anlegen und aendern koennen.

Startpunkt:

- `legacy-reference/first-try/app-mobile/kostenstelle_vorlagen.csv`
- `docs/db-schema.md`
- `supabase/schema.sql`

Akzeptanzkriterien fuer den ersten Schritt:

- Kostenstellenkatalog aus CSV kann lokal geladen oder als Seed-Struktur vorbereitet werden.
- Frontend zeigt Kostenstellen-Auswahl.
- Vorlagenmodell passt zu den bekannten Feldern: Kunde, Kostenstelle, Vorgang, Nach Aufwand, Taetigkeit, Start, Ende, Pause, Stunden.
- Keine Excel-Abhaengigkeit im neuen Workflow.

### 4. Login- und Rollenmodell vorbereiten

Ziel:

- Noch ohne echte Produktivdaten klaeren, wie Mitarbeiter, Zuweiser, Pruefer, Rike/Buero und Admin arbeiten.

Akzeptanzkriterien:

- Rollen sind im Code zentral definiert.
- Rechtepruefung ist serverseitig vorbereitet.
- Keine echte Benutzerliste oder Passwoerter im Repo.
- Supabase-App-User-Konzept bleibt kompatibel zur Plantafel.

### 5. GitHub Issues anlegen

Ziel:

- GitHub soll Arbeitszentrale werden.

Vorschlag fuer erste Issues:

- `UI: Mitarbeiter-Erfassung an First Try angleichen`
- `Feature: mehrere Stundenzeilen pro Tag`
- `Feature: Kostenstellen- und Vorlagenpflege im Admin/Buero`
- `Auth: Login und Rollenrechte vorbereiten`
- `Data: Supabase-Migration pruefen, aber noch nicht ausfuehren`
- `Workflow: Buero-/Pruefansicht am alten Viewer ausrichten`

Jedes Issue sollte kurze Akzeptanzkriterien haben.

## Noch nicht tun

- Kein Render-Deployment.
- Keine Supabase-Migration ausfuehren.
- Keine echten Mitarbeiterdaten importieren.
- Keine Excel-Pflege als neuen Dauerweg einbauen.
- Keine alten First-Try-Dateien direkt produktiv ersetzen.
- Keine Secrets in Frontend, Doku oder Commits schreiben.

## Lokale Pruefung

```powershell
python -m pip install -r requirements.txt
python -m py_compile app.py
python -m pytest
python app.py
```

Browser:

```text
http://127.0.0.1:5056
```

Hinweis: Auf diesem Windows-System kann Pytest Cache-Warnungen wegen temporaerer Cache-Ordner ausgeben. Entscheidend ist, dass die Tests selbst gruen sind.
