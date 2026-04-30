# Arbeitsregeln fuer Stundeneingabe Next Gen

## Projektquelle

- Dieses Projekt ist die zukuenftige Online-Version der Stundeneingabe.
- `Stundeneingabe First Try` bleibt bis auf Weiteres die stabile Bestandsversion.
- GitHub-Repository: `027123-prog/Zeiterfassung-Next-Gen`.
- Hosting und Datenbank werden erst festgelegt und dann hier dokumentiert.

## Vor dem Arbeiten

- `context.md` lesen.
- `tasks.md` pruefen.
- Bei Datenbank- oder Deployment-Arbeiten `docs/db-schema.md`, `docs/workflow.md` und `DEPLOYMENT.md` beachten.
- Abgrenzung zu `Stundeneingabe First Try` pruefen, bevor Bestandsdateien uebernommen oder veraendert werden.

## Dokumentation

Bei jeder Aenderung mit Projektcharakter `PROJEKTDOKUMENTATION.md` fortfuehren:

- was gemacht wurde
- warum
- wichtige Entscheidungen
- relevante Dateien
- naechste Schritte

## Sicherheit

Nie committen:

- `.env`
- Service Role Keys
- `DATABASE_URL`
- `GITHUB_TOKEN`
- Passwoerter
- personenbezogene Excel-Listen
- echte Betriebsdaten oder echte Stundenzettel
- Mail-Exporte aus dem laufenden Betrieb

## Datenbank

- Datenbankaenderungen nur bewusst durchfuehren.
- Struktur als Migration oder in `docs/db-schema.md` dokumentieren.
- `supabase/schema.sql` als Schema-Referenz aktuell halten, sobald Supabase genutzt wird.

## Tests vor Push

Vor einem Push mindestens pruefen:

- lokaler Server startet
- zentrale API-Endpunkte antworten
- Speichern und Laden funktioniert
- Login/Rollen greifen, falls vorhanden
- wichtige UI-Funktionen der Mitarbeiter- und Buero-Ansicht sind nutzbar

## GitHub

- Issues sind die Arbeitszentrale, sobald ein Repository existiert.
- Push erst nach lokaler Pruefung und Freigabe durch Nils.
