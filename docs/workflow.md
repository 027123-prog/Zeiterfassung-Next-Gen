# Workflow

## Grundsatz

`Stundeneingabe Next Gen` wird getrennt von `Stundeneingabe First Try` entwickelt. First Try bleibt produktiv mit GitHub-Mobile-App, E-Mail-Uebergabe, Thunderbird-Ablage und OneDrive-Viewer.

## Entwicklungsablauf

1. `AGENTS.md`, `context.md` und `tasks.md` lesen.
2. Offene Entscheidungen pruefen.
3. Sobald ein Repository existiert: Aufgabe ueber GitHub Issue fuehren.
4. Aenderungen lokal umsetzen.
5. Doku und `tasks.md` aktualisieren.
6. Lokal testen.
7. Erst nach Freigabe durch Nils pushen oder deployen.

## Fachlicher Zielworkflow

1. Mitarbeiter meldet sich an oder identifiziert sich eindeutig.
2. Mitarbeiter erfasst einen Arbeitstag:
   - Datum
   - Mitarbeiterkuerzel/Benutzer
   - Anfangszeit
   - Pause in ganzen Minuten
   - Endzeit
   - Stundenzeilen mit Kunde, Vorgangsnummer, Kostenstelle, Nach Aufwand, Stunden und Taetigkeit
3. System validiert Tagesdaten und Zeilen.
4. Tag wird als `submitted` gespeichert.
5. Zuweiser ordnet den Tag einem Pruefer zu.
6. Pruefer gibt frei oder fordert Aenderung an.
7. Rike/Buero markiert freigegebene Tage als eingegeben.
8. Fertig-Rolle oder Admin schliesst den Vorgang ab.

## Statusmodell

- `draft`: Mitarbeiter bearbeitet lokal/online, noch nicht eingereicht.
- `submitted`: eingereicht, wartet auf Zuweisung.
- `assigned`: einem Pruefer zugewiesen.
- `change_requested`: Pruefer fordert Korrektur.
- `approved`: freigegeben, wartet auf Rike/Buero.
- `office_entered`: von Rike/Buero eingegeben.
- `done`: abgeschlossen.
- `cancelled`: bewusst verworfen.

## Rollen

- `employee`: eigene Tage erfassen und korrigieren.
- `assigner`: eingereichte Tage zuweisen.
- `reviewer`: zugewiesene Tage pruefen, freigeben, Aenderung anfordern.
- `office`: freigegebene Tage eingeben und zurueckstellen.
- `admin`: Stammdaten, Benutzer, Rollen und Notfallkorrekturen.

Die bisherigen Viewer-Rollen werden fachlich abgebildet:

- Zuweiser -> `assigner`
- Nils R, Nils W, Matthias -> `reviewer`
- Rike -> `office`
- Fertig -> Abschlussansicht/Admin-Funktion
- Total -> Uebersicht/Auswertung

## Uebergang aus First Try

- First Try laeuft parallel weiter, bis Next Gen fachlich getestet ist.
- Mailformat und Parserregeln werden dokumentiert, aber nicht blind als neue interne Schnittstelle uebernommen.
- Optional spaeter: Import alter `.eml`-Mails in Legacy-Tabellen oder CSV-Zwischenformat.
- E-Mail-Export kann als Fallback in der Mitarbeiteransicht erhalten bleiben, muss aber bewusst entschieden werden.

## Dokumentationspflicht

Bei Aenderungen mit Projektcharakter `PROJEKTDOKUMENTATION.md` fortfuehren.

## Bestandsschutz

Dateien aus `Stundeneingabe First Try` duerfen gelesen und bewusst kopiert werden. Der laufende Bestandsablauf wird nicht veraendert.
