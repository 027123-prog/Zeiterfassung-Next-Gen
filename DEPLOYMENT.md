# Deployment

Noch kein Produktiv-Deployment. Dieses Dokument beschreibt den Zielweg nach dem Muster der Plantafel.

## Zielbild

- Runtime: Python/Flask.
- Datenbank: Supabase/Postgres.
- Hosting: voraussichtlich Render, falls Nils zustimmt.
- Healthcheck: `/api/health`.
- Frontend-Auslieferung: ueber Flask, nicht mehr ueber GitHub Pages allein.
- Codequelle: `https://github.com/027123-prog/Zeiterfassung-Next-Gen`.

## Lokaler Start

```powershell
python -m pip install -r requirements.txt
python app.py
```

Danach:

```text
http://127.0.0.1:5056
```

## Environment-Variablen

Siehe `.env.example`.

Wichtige Variablen:

- `SECRET_KEY`: Flask Session Secret.
- `SUPABASE_ENABLED`: `0` fuer lokalen Prototyp, `1` fuer Supabase.
- `SUPABASE_URL`: Supabase Projekt-URL.
- `SUPABASE_SERVICE_ROLE_KEY`: nur serverseitig setzen.
- `HOST`: lokal normalerweise `127.0.0.1`, auf Render `0.0.0.0`.
- `PORT`: lokal `5056`, auf Render vom Hoster gesetzt.

## Render-Vorschlag

Wenn Render genutzt wird:

```text
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
Health Check: /api/health
Region: Frankfurt
```

Secrets werden nicht in `render.yaml` gespeichert, sondern im Render-Dashboard gesetzt.

## Vor Push oder Deployment

Mindestens:

```powershell
python -m py_compile app.py
pytest
python app.py
```

Manuell pruefen:

- `/api/health` antwortet 200.
- `/api/config` liefert Rollen und Statuswerte.
- Demo-Frontend laedt.
- Speichern eines Demo-Tages funktioniert lokal ohne echte Betriebsdaten.
- Keine `.env`, Secrets, personenbezogenen Listen, Mail-Exporte oder echten Stundenzettel im Repository.

## Noch nicht tun

- Keine echte Datenbankmigration ausfuehren.
- Kein Render-Deployment.
- Kein Supabase-Projekt beschreiben, bevor Nils Hosting und Supabase-Ziel bestaetigt hat.
