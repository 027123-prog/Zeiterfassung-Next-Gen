# Zielarchitektur

## Leitplanken

- Neues System, kein Umbau von `Stundeneingabe First Try`.
- Muster wie Plantafel: Flask-Backend, Supabase/Postgres, Render oder vergleichbares Hosting, GitHub als Codequelle.
- Keine Secrets und keine echten Betriebsdaten im Repository.
- Datenbankstruktur dokumentiert und erst nach Zustimmung migriert.

## Komponenten

### Mitarbeiter-Frontend

- Mobile-first Weboberflaeche.
- Tagesformular mit Datum, Zeiten, Pause und Mitarbeiter.
- Wiederholbare Stundenzeilen mit Kunde, Vorgang, Kostenstelle, Nach Aufwand, Stunden und Taetigkeit.
- Kostenstellen-Picker und Vorlagen aus Datenbank.
- Validierung vor Speichern und Einreichen.
- Optionaler E-Mail-Fallback fuer Uebergangsphase.

### Buero-/Pruefansicht

- Rollenbasierte Arbeitslisten:
  - eingereicht/zuweisen
  - meine Pruefung
  - Aenderung angefordert
  - freigegeben fuer Rike/Buero
  - eingegeben/fertig
  - Total/Uebersicht
- Inline-Korrekturen mit Audit-Trail.
- Statusaktionen statt lokaler Viewer-Checkboxen.

### API

- Flask liefert Frontend und JSON-API aus.
- Serverseitige Session/Auth analog Plantafel.
- Supabase-Zugriff nur serverseitig mit Service Role Key.
- Zentrale Validierungsfunktionen fuer Zeiten, Pause, Stunden, Vorgangsnummer und Statusuebergaenge.

Startpunkte im Prototyp:

- `GET /api/health`
- `GET /api/config`
- `GET /api/days`
- `POST /api/days`

Spaetere API:

- `/api/login`, `/api/logout`, `/api/me`
- `/api/employees`
- `/api/cost-centers`
- `/api/templates`
- `/api/timesheet-days`
- `/api/timesheet-days/<id>/submit`
- `/api/timesheet-days/<id>/assign`
- `/api/timesheet-days/<id>/approve`
- `/api/timesheet-days/<id>/request-change`
- `/api/timesheet-days/<id>/office-entered`
- `/api/timesheet-days/<id>/done`

## Datenbankmodell

Kern:

- `employees`
- `app_users`
- `cost_centers`
- `cost_center_templates`
- `timesheet_days`
- `time_entries`
- `workflow_events`
- `legacy_mail_imports`

Details stehen in `docs/db-schema.md` und `supabase/schema.sql`.

## Rollen und Rechte

- `employee`: eigene Tage anlegen, bearbeiten, einreichen, Aenderungsanforderungen beantworten.
- `assigner`: eingereichte Tage Pruefern zuweisen.
- `reviewer`: zugewiesene Tage pruefen, korrigieren, freigeben oder Aenderung anfordern.
- `office`: freigegebene Tage als eingegeben markieren, bei Bedarf zurueckstellen.
- `admin`: Stammdaten, Benutzer, Notfallkorrekturen und Abschluss.

## Import-/Uebergangsstrategie

Phase 1:

- First Try unveraendert produktiv lassen.
- Next Gen lokal und spaeter online parallel aufbauen.
- Keine alten Mails automatisch importieren.

Phase 2:

- Kostenstellenkatalog und vorhandene CSV-Vorlagen bewusst importieren.
- Neue und geaenderte Vorlagen sollen spaeter in der Admin-/Buero-Weboberflaeche gepflegt werden, nicht ueber Excel-Dateien im Repository.
- Mitarbeiter und Benutzer aus einer separaten, nicht committed Benutzerliste anlegen.

Phase 3:

- Optionaler Import alter E-Mails:
  - `.eml` lesen
  - Betreff/Message-ID/Body-Hash speichern
  - Parserwarnungen sichtbar machen
  - importierte Tage als `source = first-try-mail` markieren

Phase 4:

- Pilotbetrieb mit ausgewählten Mitarbeitern.
- E-Mail-Fallback so lange erhalten, bis Freigabe durch Nils erfolgt.

## Hosting/Deployment

Vorschlag:

- Neues GitHub-Repository fuer dieses Projekt.
- Render Web Service analog Plantafel.
- Supabase als separate Datenbank.
- `/api/health` als Healthcheck.
- `gunicorn app:app --bind 0.0.0.0:$PORT` als Startkommando.

Blocker vor echtem Deployment:

- Repository-Name.
- Supabase-Projekt.
- Hosting-Ziel.
- Secrets/Environment-Werte.
- Initiale Benutzer- und Rollenliste.
