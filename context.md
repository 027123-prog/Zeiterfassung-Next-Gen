# Kontext: Stundeneingabe Next Gen

## Ausgangslage

Die aktuelle Stundeneingabe laeuft als `Stundeneingabe First Try` und bleibt bis zur bewussten Abloesung produktiv.

- Mitarbeiter nutzen `app-mobile/index.html`, inhaltlich gespiegelt von `stunden_app_mobile.html`.
- Die App speichert lokal im Browser unter `time_entries_mail_v4`.
- Uebergabe erfolgt per E-Mail an `info@roewekamp-stumpe.de`.
- Betreffmuster: `KUERZEL DD.MM.YYYY Stundenzettel Kunde`.
- Thunderbird legt passende `.eml`-Dateien im OneDrive-Ordner `@ Stundenzettel` ab.
- Der Viewer `office_mail_viewer.html` liest Mails, parst Stundenzeilen und speichert Workflow-State in `viewer_data/office_state.json`.
- Kostenstellen-Vorlagen stammen fachlich aus `kostenstelle_vorlagen_editor.xlsx`, technisch als `kostenstelle_vorlagen.csv`.

## Erkenntnisse aus First Try

- Mobile-App-Version: `APP_VERSION = V1.6`.
- Viewer-Version: `VIEWER_VERSION = V1.21`.
- Export kennt ein kompaktes Tagesformat mit Tagesdefaults plus Zeilen und `#RS#` als Zeilen-Endmarker.
- Vollformat nutzt Spalten: Datum, Mitarbeiterkuerzel, Anfangszeit, Pause, Endzeit, Kundenname, Vorgangsnr., Kostenstelle, Nach Aufwand?, Stunden, Taetigkeit.
- Wichtige Validierungen: Datum Pflicht, Mitarbeiterkuerzel Pflicht, Vorgangsnummer optional aber wenn vorhanden `YYVG0NNN`, Pause ganze Minuten >= 0, Stunden > 0, Start/Ende/Pause muessen plausible Nettozeit ergeben.
- Viewer-Rollen: Zuweiser, Nils R, Nils W, Matthias, Rike, Fertig, Total.
- Workflow im Viewer: unzugewiesen -> zugewiesen -> freigegeben oder Aenderung angefordert -> Rike/eingegeben -> Fertig; Rueckgaben sind moeglich.
- Bekannte Fehlerklassen: Mailclient-Encoding, harte Umbrueche, abgeschnittene Aktivitaet, alte App-Versionen im Cache, inkonsistenter Viewer-State.

## Plantafel-Muster

- Flask-App liefert Frontend und API aus.
- Supabase/Postgres ist Live-Datenbank.
- Render ist naheliegendes Hosting mit `/api/health` als Healthcheck.
- Geheimnisse bleiben serverseitig in `.env` oder Hoster-Environment.
- Lokale Tests und Dokumentation sind Pflicht vor Push.
- GitHub Issues werden Arbeitszentrale, sobald ein neues Repository existiert.

## Projektquelle

- GitHub-Repository: `027123-prog/Zeiterfassung-Next-Gen`.
- `main` ist der gemeinsame Arbeitsstand fuer die erste Projektgrundlage.
- Es gibt noch kein Produktiv-Deployment und keine echte Supabase-Migration.
- `legacy-reference/first-try` enthaelt bewusst kopierte Referenzdateien aus First Try fuer Analyse und Abgleich.

## Ziel

Die Stundenaufstellung wird als neues Online-System gebaut. First Try wird nicht umgebaut. Uebernahmen aus First Try werden bewusst kopiert, angepasst und dokumentiert.

## Offene Entscheidungen

- Supabase-Projekt oder bestaetigte Wiederverwendung eines bestehenden Projekts.
- Hosting-Ziel, vermutlich Render analog Plantafel.
- Finale Rollen-/Benutzerliste und Authentifizierung.
- Uebergangsphase: reiner Parallelbetrieb, Import alter Mails oder E-Mail-Fallback.
