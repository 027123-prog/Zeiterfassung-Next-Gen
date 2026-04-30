# Bestandsanalyse: Stundeneingabe First Try

Stand der Analyse: 2026-04-30.

## Gelesene Quellen

- `app-mobile/stunden_app_mobile.html`
- `app-mobile/index.html`
- `app-mobile/kostenstelle_vorlagen.csv`
- `app-mobile/kostenstelle_vorlagen_editor.xlsx` als fachlich fuehrende Vorlage, nicht inhaltlich geoeffnet
- `viewer/office_mail_viewer.html`
- `docs/SYSTEM_OVERVIEW.md`
- `docs/TECHNICAL_JOURNAL.md`
- `docs/DEPLOYMENT_ONEDRIVE_GITHUB.md`
- `archive/UEBERGABE_PROJEKT_2026-03-09.md`

## Aktueller Ablauf

1. Mitarbeiter erfasst einen Tag in der mobilen HTML-App.
2. Die App speichert Entwuerfe lokal im Browser.
3. Beim Versand erzeugt die App einen E-Mail-Text und Betreff.
4. Mail geht an `info@roewekamp-stumpe.de`.
5. Thunderbird legt passende Mails im OneDrive-Ordner `@ Stundenzettel` ab.
6. Der Viewer liest `.eml`/`.txt`, parst Zeilen und dedupliziert neue Versionen.
7. Workflow-Status wird in `viewer_data/office_state.json` gespeichert.
8. Rollen arbeiten im Viewer auf gefilterten Sichten.

## Mobile-App

- Aktuelle Version: `V1.6`.
- Fuehrende Datei: `app-mobile/stunden_app_mobile.html`.
- GitHub-Pages-Datei: `app-mobile/index.html`, soll identisch sein.
- Lokaler Speicher: `time_entries_mail_v4`, mit Legacy-Keys `time_entries_mail_v3`, `time_entries_mail_v2`, `time_entries_mail_v1`, `time_entries_mail`.
- Office-Adresse: `info@roewekamp-stumpe.de`.
- Maximaler Direkt-`mailto`-Text: 1800 Zeichen, danach Fallback ueber Zwischenablage.

## Eingabefelder

- Datum
- Mitarbeiterkuerzel
- Anfangszeit
- Pause in Minuten
- Endzeit
- Kundenname
- Vorgangsnr. aus `YY` + `VG0` + dreistelligem Suffix
- Kostenstelle
- Nach Aufwand?
- Stunden
- Taetigkeit

## Validierungen

- Datum ist Pflicht.
- Mitarbeiterkuerzel ist Pflicht und wird normalisiert.
- Vorgangsnummer ist optional; wenn vorhanden, muss sie `YYVG0NNN` entsprechen.
- `YYVG0` ohne Suffix gilt als leer.
- Pause muss eine ganze Minutenzahl >= 0 sein.
- Stunden muessen als Zahl > 0 eingegeben werden, Komma und Punkt sind erlaubt.
- Anfangszeit, Endzeit und Pause duerfen keine negative Nettozeit ergeben.
- Versand eines Tages wird blockiert, wenn Zeilenstunden ungueltig sind, Tagesdaten uneinheitlich sind oder Soll/Ist nicht plausibel ist.

## Exportformat

Betreff:

```text
KUERZEL DD.MM.YYYY Stundenzettel Kundenname
```

Kompaktes Tagesformat:

```text
V1.6
YYYY-MM-DD KUERZEL HH:MM PAUSE HH:MM KONTROLLSTUNDEN
Kunde Vorgang Kostenstelle NachAufwand Stunden Taetigkeit #RS#
```

Vollformat:

```text
Datum	Mitarbeiterkuerzel	Anfangszeit	Pause (Min)	Endzeit	Kundenname	Vorgangsnr.	Kostenstelle	Nach Aufwand?	Stunden	Taetigkeit
```

Der Marker `#RS#` beendet Datenzeilen und hilft dem Viewer gegen harte Mail-Umbrueche.

## Kostenstellen und Vorlagen

- Fachlich fuehrend: `kostenstelle_vorlagen_editor.xlsx`.
- Technische Quelle fuer die Mobile-App: `kostenstelle_vorlagen.csv`.
- Excel-Struktur:
  - Sheet `1_Vorlagen_Eingabe`: Vorlage-Buttons, 500 Zeilen, 11 Spalten.
  - Sheet `2_Kostenstellen`: Kostenstellen-Katalog, 42 Zeilen, 4 Spalten.
- CSV-Spalten: Buttonname, Kunde, Kostenstelle, VorgangsPraefix, VorgangSuffix, NachAufwand, Taetigkeit, Startzeit, Endzeit, Pause, Stunden.
- Excel-Hinweis: Pflichtfelder der Vorlagen sind Buttonname, Kostenstelle und Taetigkeit. Werte werden als Text behandelt, damit fuehrende Nullen wie `0016` erhalten bleiben.
- Die App laedt die CSV per `fetch`, hat aber eingebettete Default-Vorlagen als Fallback.
- Kostenstellen sind dreistellige Codes, z. B. `FWS`, `SIU`, `ORD`, `IWS`.

## Viewer

- Aktuelle Version: `V1.21`.
- Fuehrende Entwicklungsdatei: `viewer/office_mail_viewer.html`.
- Produktiver Pfad laut Doku: `C:\Users\Nils Wienstroer\OneDrive\@ Stundenzettel\office_mail_viewer.html`.
- Persistenz: `viewer_data/office_state.json`, Fallback in `localStorage`.
- Parser behandelt MIME-Headers, encoded words, quoted-printable, base64/html-only, harte Umbrueche und Mail-Signaturen.
- Deduplizierung/versionierte Uebernahme nutzt Betreff, Message-ID und interne Zeilenschluessel.

## Rollenmodell im Viewer

- `Zuweiser`: sieht unzugewiesene Zeilen/Tage und weist Pruefern zu.
- `Nils R`, `Nils W`, `Matthias`: pruefen zugewiesene Zeilen, bearbeiten, freigeben oder Aenderung anfordern.
- `Rike`: sieht freigegebene Zeilen und markiert sie als eingegeben.
- `Fertig`: Abschluss-/Rueckgabeansicht nach Rike.
- `Total`: Gesamtuebersicht und Controlling.

## Statuslogik

Technisch sind im Viewer vor allem diese Flags relevant:

- `assignedTo`
- `checked`
- `changeRequested`
- `enteredByRike`
- `deleted`

Fachlich ergibt sich:

- unzugewiesen
- zugewiesen
- freigegeben
- Aenderung angefordert
- Rike/Buero eingegeben
- fertig/abgeschlossen

Rueckgaben sind vorgesehen: Pruefer kann zurueck an Zuweiser, Rike kann zurueck an Kontrollierer, Fertig kann zurueck an Rike.

## Bekannte Fehlerklassen

- Aktivitaet abgeschnitten oder durch CSS/Parser optisch abgeschnitten.
- Zeilen werden bei harten Umbruechen verschluckt.
- Mailclients veraendern Text durch quoted-printable, base64 oder HTML-only.
- Alte App-Versionen senden Altschema wegen Browser-Cache oder altem Tab.
- Viewer-State kann bei fehlendem Ordner-Handle nur lokal im Browser liegen.

## Konsequenzen fuer Next Gen

- Mailtext wird nicht mehr primaere Datenhaltung.
- Tages- und Zeilenmodell muss direkt in der Datenbank liegen.
- Workflow-Status wird explizit als Datenbankstatus plus Audit-Events modelliert.
- Kostenstellen und Vorlagen werden Stammdaten.
- Parserwissen bleibt wichtig fuer Uebergang/Import, aber nicht fuer den Kernablauf.
- Validierungsregeln aus der Mobile-App werden serverseitig nachgebaut.
