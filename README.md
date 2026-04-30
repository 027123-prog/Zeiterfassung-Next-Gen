# Stundeneingabe Next Gen

`Stundeneingabe Next Gen` ist die getrennte Neuentwicklung der bisherigen Stundeneingabe als online laufende Anwendung.

Die stabile Bestandsloesung bleibt in `Stundeneingabe First Try`: Mitarbeiter erfassen Stunden ueber die GitHub-gehostete Mobile-App, verschicken einen E-Mail-Text, Thunderbird legt Mails ab und der Viewer im OneDrive prueft und verarbeitet diese Mails.

Repository:

```text
https://github.com/027123-prog/Zeiterfassung-Next-Gen
```

## Zielbild

- Mitarbeiter erfassen Tagesdaten und Stundenzeilen online.
- Buero, Zuweiser, Pruefer, Rike und Fertig-Rolle arbeiten auf denselben Daten.
- Status, Freigaben und Aenderungsanforderungen werden in der Datenbank statt in Mail-/Viewer-State gehalten.
- E-Mail-Export und Import aus First Try bleiben fuer die Uebergangsphase fachlich dokumentiert.
- Code, Datenbankstruktur, Runtime und Deployment sind aus dem Repository rekonstruierbar.

## Lokaler Start

```powershell
python -m pip install -r requirements.txt
python app.py
```

Danach:

```text
http://127.0.0.1:5056
```

Der aktuelle Prototyp speichert noch keine Produktivdaten. Supabase ist nur als serverseitiger Platzhalter vorbereitet.

## API-Startpunkte

- `GET /api/health`: Healthcheck.
- `GET /api/config`: Rollen, Statuswerte und Betriebsmodus.
- `GET /api/days`: lokale Demo-/API-Struktur fuer Stundentage.
- `POST /api/days`: validiert einen Beispiel-Stundentag und speichert ihn lokal, solange Supabase nicht aktiviert ist.

## Orientierung

- `context.md`: Projektkontext und Bestandsanalyse.
- `tasks.md`: Aufgaben und offene Entscheidungen.
- `PROJEKTDOKUMENTATION.md`: laufende Projektdokumentation.
- `docs/workflow.md`: Arbeitsweise, Uebergang und Freigabeablauf.
- `docs/db-schema.md`: Ziel-Datenmodell.
- `docs/bestandsanalyse-first-try.md`: Analyse der aktuellen Loesung.
- `docs/architecture.md`: Zielarchitektur fuer Next Gen.
- `DEPLOYMENT.md`: Hosting und Runtime.
- `supabase/schema.sql`: Schema-Referenz, noch nicht angewendet.

## Sicherheit

Keine echten Betriebsdaten, Mail-Exporte, personenbezogenen Excel-Listen, `.env`-Dateien oder Secrets ins Repository legen. Eine echte Supabase-Migration und ein Push erfolgen erst nach Zustimmung von Nils.
