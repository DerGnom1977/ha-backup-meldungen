# Backup-Meldungen

![Backup-Meldungen](https://raw.githubusercontent.com/DerGnom1977/ha-backup-meldungen/main/images/preview.png)

Meldet fehlgeschlagene oder überfällige Home-Assistant-Backups per Push.

![Dashboard](https://raw.githubusercontent.com/DerGnom1977/ha-backup-meldungen/main/images/dashboard.jpg)

Python-Integration für Home Assistant (HACS). Sie ersetzt das bisherige YAML-Paket
`backup/packages/backup_benachrichtigung.yaml`: Einstellungen sind jetzt eigene Entitäten (Schalter, Zahlen, Auswahlfelder,
Uhrzeiten), die Logik läuft in Python statt in Automationen und Skripten.

## Installation

1. HACS → Integrationen → ⋮ → **Benutzerdefinierte Repositories** →
   `https://github.com/DerGnom1977/ha-backup-meldungen` als Kategorie **Integration** hinzufügen.
2. **Backup-Meldungen** installieren und Home Assistant neu starten.
3. Einstellungen → Geräte & Dienste → **Integration hinzufügen** → *Backup-Meldungen*.
4. Das Dashboard aus `dashboards/backup_meldungen_dashboard.yaml` anlegen (Raw-Konfigurationseditor).

Manuell: Ordner `custom_components/backup_meldungen` nach `/config/custom_components/` kopieren.

## Einrichtung

Beim Hinzufügen (und später über „Konfigurieren“) werden diese Angaben abgefragt:

- **Notify-Dienst Person 1** (`notify_person1`), Standard: `mobile_app_mein_handy`
- **Notify-Dienst Person 2** (`notify_person2`), Standard: `mobile_app_partner_handy`
- **Backup-Ereignis** (`event_entity`), Standard: `event.backup_automatisches_backup`
- **Letztes erfolgreiches Backup** (`last_success`), Standard: `sensor.backup_letztes_erfolgreiches_automatisches_backup`
- **Größe des letzten Backups** (`size_entity`), Standard: `sensor.backup_grosse_des_letzten_erfolgreichen_automatischen_backups`

## Was du anpassen musst

Alle Standardwerte oben sind **Platzhalter/Beispiele**. Passe sie beim Einrichten an dein System an:

- **Notify-Dienste** (`notify_person1`, `notify_person2`): Name deines Handy-Dienstes ohne `notify.`,
  z. B. `mobile_app_mein_handy` → bei dir `mobile_app_<gerätename>` (Entwicklerwerkzeuge → Aktionen → „notify“).
  „Person 1/Person 2“ sind frei; die Schalter *Push an Person 1/2* schalten die jeweilige Meldung.
- **Entitäten** (`sensor.…`, `camera.…`, `person.…`, `todo.…` usw.): auf die echten Entitäts-IDs aus
  Einstellungen → Geräte & Dienste → Entitäten ändern. Leere Felder sind Pflicht, wenn die Funktion genutzt wird.
- **Dashboard** (`dashboards/backup_meldungen_dashboard.yaml`): enthält Entitäts-IDs der Integration; wenn du Namen
  oder Räume änderst, dort per Suchen/Ersetzen nachziehen.
- Später jederzeit unter Einstellungen → Geräte & Dienste → *Backup-Meldungen* → **Konfigurieren** änderbar.

## Umstieg vom YAML-Paket

1. Das alte Paket `backup/packages/backup_benachrichtigung.yaml` (und sein Dashboard) aus `/config/packages/` entfernen
   und Home Assistant neu starten, damit Helfer, Automationen und Skripte nicht doppelt laufen.
2. Integration einrichten. Neue Entitäten haben dieselben Namen wie die alten Helfer, nur mit
   anderer Domain, z. B. `input_boolean.xyz` wird `switch.xyz`, `input_number.xyz` wird `number.xyz`,
   `input_select.xyz` wird `select.xyz`, `input_datetime.xyz` wird `time.xyz`.
3. Eigene Automationen und Dashboards, die alte Entitäten nutzen, entsprechend anpassen.
4. Die alten Standardwerte sind schon eingebaut, die Einstellungen bleiben nach Neustarts erhalten.

## Entitäten

### Schalter

- `switch.backup_push_aktiv` – Backup-Meldungen aktiv
- `switch.backup_ziel_person1` – Backup-Push an Person 1
- `switch.backup_ziel_person2` – Backup-Push an Person 2
- `switch.backup_bei_erfolg` – Auch bei Erfolg melden

### Zahlenwerte

- `number.backup_max_alter_tage` – Warnen, wenn letztes Backup älter als

### Sensoren

- `sensor.backup_alter_tage` – Alter des letzten Backups

### Knöpfe

- `button.backup_test` – Testmeldung senden
- `button.backup_standardwerte` – Standardwerte setzen

## Hinweis

Die Integration wurde aus dem bestehenden YAML-Paket portiert und ist noch nicht in einer laufenden
Home-Assistant-Instanz getestet. Bitte beim ersten Einsatz die Logbuch-/Protokoll-Meldungen
(`custom_components.backup_meldungen`) im Blick behalten.
