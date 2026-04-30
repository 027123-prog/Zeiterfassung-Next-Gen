# Projektdokumentation: Stundeneingabe Next Gen

## 2026-04-30: Projektgrundlage angelegt

### Was gemacht wurde

Die Grundstruktur fuer `Stundeneingabe Next Gen` wurde unter `Codex\Projekte\aktiv` angelegt.

Angelegt wurden:

- `AGENTS.md`
- `README.md`
- `context.md`
- `tasks.md`
- `PROJEKTDOKUMENTATION.md`
- `DEPLOYMENT.md`
- `docs/workflow.md`
- `docs/db-schema.md`
- `supabase/schema.sql`
- `data/.gitkeep`
- `tests/.gitkeep`

### Warum

Nils moechte die bisherige Stundenaufstellung perspektivisch nach dem Muster der Plantafel komplett online bringen. Die bestehende Loesung soll aber unter `Stundeneingabe First Try` stabil weiterlaufen.

### Wichtige Entscheidungen

- `First Try` bleibt Bestandsprojekt und wird nicht zur Experimentierflaeche.
- `Next Gen` ist ein neues, getrenntes Projekt fuer die Online-Architektur.
- Die Arbeitsweise orientiert sich an der Plantafel: Kontextdatei, Aufgabenliste, Projektdoku, Datenbankdoku, Deploymentdoku, GitHub Issues und lokale Pruefung vor Push.

### Relevante Dateien

- `context.md`: aktueller Projektkontext und Zielbild
- `tasks.md`: naechste Aufgaben
- `AGENTS.md`: Arbeitsregeln fuer Codex

### Naechste Schritte

- Fachlichen Soll-Ablauf mit Nils klaeren.
- Repository und Hosting-Ziel festlegen.
- Datenmodell und Rollenmodell entwerfen.

## 2026-04-30: Bestandsanalyse und Start-Prototyp

### Was gemacht wurde

First Try wurde fachlich und technisch ausgewertet. Plantafel wurde als Muster fuer Flask, Supabase, Render, Doku und Tests gelesen. In Next Gen wurden Doku, Schema-Entwurf und ein minimaler lokaler Flask-Prototyp angelegt.

Angelegt oder aktualisiert wurden:

- `README.md`
- `context.md`
- `tasks.md`
- `DEPLOYMENT.md`
- `docs/workflow.md`
- `docs/db-schema.md`
- `docs/bestandsanalyse-first-try.md`
- `docs/architecture.md`
- `supabase/schema.sql`
- `.env.example`
- `.gitignore`
- `requirements.txt`
- `render.yaml`
- `app.py`
- `index.html`
- `tests/test_app.py`

### Warum

Nils moechte die bisherige Stundeneingabe als getrenntes neues Online-System nach dem Muster der Plantafel aufbauen. Die alte Loesung soll stabil bleiben und nicht versehentlich zur Experimentierflaeche werden.

### Erkenntnisse

- First Try arbeitet ueber Mobile-App, E-Mail-Text, Thunderbird-Ablage und OneDrive-Viewer.
- Der aktuelle Export enthaelt Version `V1.6`, kompakte Tagesdaten, Kostenstelle, Nach Aufwand, Stunden und den Zeilen-Endmarker `#RS#`.
- Der Viewer `V1.21` bildet Rollen und Status ueber lokalen/OneDrive-Status ab.
- Kostenstellenvorlagen kommen fachlich aus Excel und technisch aus CSV.
- Relevante Fehlerklassen sind Mail-Encoding, harte Umbrueche, alte App-Versionen, abgeschnittene Aktivitaet und lokaler Viewer-State.

### Wichtige Entscheidungen

- Next Gen bekommt ein explizites Tages-/Zeilenmodell in Supabase statt Mailtext als Primaerdaten.
- Workflow wird als Status plus Audit-Events modelliert.
- Rollen werden aus dem Viewer abgeleitet: employee, assigner, reviewer, office, admin.
- Supabase-Schema wurde nur als Referenz geschrieben, nicht migriert.
- Der lokale Prototyp speichert nur Demo-Daten in `data/timesheet_days.local.json`, die per `.gitignore` ausgeschlossen sind.

### Relevante Dateien

- `docs/bestandsanalyse-first-try.md`: fachliche Analyse der alten Loesung.
- `docs/architecture.md`: Zielarchitektur.
- `supabase/schema.sql`: Datenbankentwurf.
- `app.py`: Flask-Prototyp mit Healthcheck und API-Grundstruktur.
- `index.html`: statisches Demo-Frontend.
- `tests/test_app.py`: erste API-/Validierungstests.

### Naechste Schritte

- Nils bestaetigt Repository-Name, Supabase-Projekt und Hosting-Ziel.
- GitHub-Repository anlegen und Issues als Arbeitszentrale nutzen.
- Login/Rollen ausbauen.
- Mitarbeiter- und Buero-/Pruefansicht fachlich ausbauen.
- Kostenstellen- und Vorlagenimport aus CSV/Excel bewusst planen.

## 2026-04-30: Lokaler Workflow-Prototyp erweitert

### Was gemacht wurde

Der lokale Flask-Prototyp wurde um Workflow-Aktionen erweitert. Das Frontend zeigt jetzt neben der Mitarbeiter-Erfassung eine einfache Buero-/Pruefansicht mit Ansichten fuer Zuweiser, Pruefung, Aenderung, Rike/Buero, Eingegeben, Fertig und Total.

### Warum

Nach dem erfolgreichen Speichern eines Demo-Tags sollte der naechste fachliche Schritt nicht nur ein weiteres Formular sein, sondern der eigentliche Viewer-Ablauf aus First Try: Zuweisen, Pruefen, Freigeben, Aenderung anfordern, Rike/Buero und Fertig.

### Wichtige Entscheidungen

- Der Workflow bleibt lokal und prototypisch.
- Es gibt noch keinen echten Login; Aktionen laufen als `lokaler Prototyp`.
- Pruefer sind im Prototyp als `Nils R`, `Nils W` und `Matthias` hinterlegt.
- Jede Workflow-Aktion schreibt ein `workflowEvents`-Audit-Event an den lokalen Demo-Tag.

### Relevante Dateien

- `app.py`: Workflow-Aktionen und API `POST /api/days/<id>/workflow`.
- `index.html`: Buero-/Pruefansicht und Statusaktionen.
- `tests/test_app.py`: Tests fuer Zuweisung und ungueltige Statusuebergaenge.
- `tasks.md`: Fortschritt aktualisiert.

### Naechste Schritte

- Echte Login-/Rollenlogik ausarbeiten.
- Mehrere Stundenzeilen pro Tag im Frontend bedienbar machen.
- Kostenstellenkatalog und Vorlagen in die Erfassung einbauen.
- Danach erst Supabase-Anbindung planen und von Nils freigeben lassen.

## 2026-04-30: GitHub-Veröffentlichung vorbereitet

### Was gemacht wurde

Der Projektstand wurde fuer GitHub vorbereitet und als Initial-Commit in `027123-prog/Zeiterfassung-Next-Gen` veroeffentlicht. Die Doku wurde auf dieses Repository aktualisiert.

### Warum

Nils moechte am Wochenende mit anderen Agenten am Projekt weiterarbeiten. Dafuer muss der komplette Projektstand zentral in GitHub liegen.

### Wichtige Entscheidungen

- Lokale Demo-Daten, Logs, Pycache, Pytest-Tempdaten und echte Betriebsdaten bleiben durch `.gitignore` ausgeschlossen.
- `supabase/schema.sql` bleibt nur Schema-Referenz, keine angewendete Migration.
- Hosting und Supabase-Ziel bleiben offen.

### Relevante Dateien

- `README.md`
- `context.md`
- `tasks.md`
- `DEPLOYMENT.md`
- `.gitignore`

### Naechste Schritte

- Erste GitHub-Issues mit Akzeptanzkriterien anlegen.
