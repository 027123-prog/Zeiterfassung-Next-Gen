# Legacy-Referenzen

Dieser Ordner enthaelt bewusst kopierte Referenzdateien aus `Stundeneingabe First Try`.

## Zweck

Andere Agenten sollen am Wochenende die alte Mitarbeiter-Eingabe, den alten Viewer, die Kostenstellenlogik und die Vorlagenstruktur direkt im Repository nachlesen koennen, ohne das produktive First-Try-Projekt anzufassen.

## Regeln

- Diese Dateien sind Referenzkopien, keine neue Produktivquelle.
- `Stundeneingabe First Try` bleibt stabil und wird nicht aus diesem Ordner heraus deployed.
- Aenderungen fuer Next Gen werden in der neuen Flask-/API-Struktur umgesetzt, nicht blind in den Legacy-Dateien.
- Wenn fachliche Logik uebernommen wird, wird sie bewusst kopiert, angepasst und dokumentiert.

## Inhalt

- `first-try/app-mobile/stunden_app_mobile.html`: aktuelle mobile Eingabe-App aus First Try.
- `first-try/app-mobile/index.html`: GitHub-Pages-Spiegel der mobilen Eingabe.
- `first-try/app-mobile/kostenstelle_vorlagen.csv`: technische Quelle der Vorlagenbuttons.
- Die alte Excel-Vorlage wird nicht ins Repo uebernommen. In Next Gen sollen Vorlagen spaeter ueber die Admin-/Buero-Weboberflaeche gepflegt werden.
- `first-try/app-mobile/kostenstelle_auswahl_demo.html`: Kostenstellen-Auswahldemo.
- `first-try/app-mobile/app.js` und `styles.css`: alte/fruehere App-Dateien aus First Try.
- `first-try/viewer/office_mail_viewer.html`: alter OneDrive-/Mail-Viewer.
