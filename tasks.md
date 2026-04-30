# Stundeneingabe Next Gen Aufgaben

## Jetzt

- [x] Eigenes Projekt fuer die Online-Neuentwicklung anlegen.
- [x] Abgrenzung zu `Stundeneingabe First Try` dokumentieren.
- [x] First-Try-Bestand fachlich auswerten.
- [x] Plantafel-Workflow auf dieses Projekt uebertragen.
- [x] Zielarchitektur und Datenmodell vorschlagen.
- [x] Minimalen lokalen Prototyp mit Healthcheck/API-Grundstruktur anlegen.
- [x] Lokalen Workflow-Prototyp fuer Zuweisung, Pruefung, Rike/Buero und Fertig anlegen.
- [x] GitHub-Repository fuer Wochenend-Arbeit vorbereiten: `027123-prog/Zeiterfassung-Next-Gen`.
- [x] First-Try-Eingabe, Viewer und CSV-Vorlagendatei als Referenzkopien ins Repo legen.
- [x] Briefing fuer naechste Agenten mit sinnvollen Schritten dokumentieren.
- [ ] Fachlichen Soll-Ablauf mit Nils klaeren.
- [ ] Hosting-Ziel festlegen.

## Kurzfristig

- [x] GitHub-Repository anlegen.
- [ ] Erste GitHub-Issues mit Akzeptanzkriterien anlegen.
- [x] Datenmodell fuer Mitarbeiter, Tage, Stundenzeilen, Kostenstellen, Freigaben und Status entwerfen.
- [x] Rollenmodell definieren: Mitarbeiter, Zuweiser/Pruefer, Buero/Rike, Admin.
- [x] Bestands-App und Viewer aus `First Try` fachlich auswerten.
- [ ] Login gegen Supabase-App-Benutzer umsetzen.
- [ ] Mitarbeiter-Frontend aus Prototyp zu echter Erfassung ausbauen.
- [x] Erste Buero-/Pruefansicht als lokale Arbeitsliste anlegen.
- [ ] Kostenstellenkatalog und Vorlagen importierbar machen.
- [ ] Admin-/Buero-Oberflaeche fuer Kostenstellen- und Vorlagenpflege entwerfen.
- [ ] Importstrategie fuer First-Try-Mails entscheiden.
- [x] Tests fuer Validierungen und lokale Workflow-Aktionen erweitern.

## Fachliche Punkte

- [ ] Wie Mitarbeiter sich identifizieren oder anmelden.
- [x] Wie Tagesdaten, Pausen, Zeiten und Stunden initial validiert werden.
- [x] Wie Kostenstellen gepflegt werden sollen.
- [x] Wie Freigabe, Aenderungsanforderung und Fertigmeldung online ablaufen.
- [ ] Welche Auswertungen das Buero braucht.
- [ ] Ob E-Mail-Export als Fallback erhalten bleibt und fuer wen.
- [ ] Ob Prueferrollen namentlich bleiben: Nils R, Nils W, Matthias.
- [ ] Welche Mitarbeiterkuerzel und Login-Namen initial angelegt werden.

## Spaeter

- [ ] Supabase-/Datenbankmigrationen erstellen.
- [ ] Lokale Tests und API-Tests einrichten.
- [ ] Deployment dokumentieren.
- [ ] Backup- und Restore-Ablauf dokumentieren.
- [ ] Uebergangsphase von `First Try` zu `Next Gen` planen.

## Empfohlene Reihenfolge fuer naechste Agenten

1. Mitarbeiter-UI naeher an First Try bringen.
2. Mehrere Stundenzeilen pro Tag umsetzen.
3. Kostenstellen- und Vorlagenpflege fuer Admin/Buero entwerfen.
4. Login- und Rollenrechte vorbereiten.
5. GitHub Issues mit Akzeptanzkriterien anlegen.

Details stehen in `docs/next-agent-briefing.md`.
