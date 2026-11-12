"""Backup-Meldungen: Spezifikation."""
from __future__ import annotations

from homeassistant.util import dt as dt_util

from .framework import Field, Spec

DOMAIN = "backup_meldungen"
TITLE = "Backup-Meldungen"
PREFIX = "backup"
VERSION = "1.0.0"
DESCRIPTION = "Meldet fehlgeschlagene oder überfällige Home-Assistant-Backups per Push."
DASHBOARD_PATH = "dashboard-backup"

FIELDS = [
    Field("notify_person1", "mobile_app_mein_handy", "text", "Notify-Dienst Person 1"),
    Field("notify_person2", "mobile_app_partner_handy", "text", "Notify-Dienst Person 2"),
    Field("event_entity", "event.backup_automatisches_backup", "entity", "Backup-Ereignis", ("event",)),
    Field("last_success", "sensor.backup_letztes_erfolgreiches_automatisches_backup", "entity", "Letztes erfolgreiches Backup", ("sensor",)),
    Field("size_entity", "sensor.backup_grosse_des_letzten_erfolgreichen_automatischen_backups", "entity", "Größe des letzten Backups", ("sensor",)),
]


def letztes(rt):
    return dt_util.parse_datetime(rt.state(rt.cfg("last_success")) or "")


def alter_tage(rt):
    ts = letztes(rt)
    if ts is None:
        return None
    return round((dt_util.utcnow() - ts).total_seconds() / 86400, 1)


def letztes_text(rt) -> str:
    ts = letztes(rt)
    return dt_util.as_local(ts).strftime("%d.%m.%Y %H:%M") if ts else "unbekannt"


SPECS = [
    Spec("switch", "backup_push_aktiv", "Backup-Meldungen aktiv", "mdi:backup-restore", True),
    Spec("switch", "backup_ziel_person1", "Backup-Push an Person 1", "mdi:cellphone-message", True),
    Spec("switch", "backup_ziel_person2", "Backup-Push an Person 2", "mdi:cellphone-message", True),
    Spec("switch", "backup_bei_erfolg", "Auch bei Erfolg melden", "mdi:check-circle-outline", False),
    Spec("number", "backup_max_alter_tage", "Warnen, wenn letztes Backup älter als", "mdi:calendar-alert", 9, 2, 30, 1, "d", "slider"),
    Spec("sensor", "backup_alter_tage", "Alter des letzten Backups", "mdi:calendar-clock", unit="d", fn=alter_tage),
    Spec("button", "backup_test", "Testmeldung senden", "mdi:bell-check", press="test"),
    Spec("button", "backup_standardwerte", "Standardwerte setzen", "mdi:restore", press="reset"),
]

SECTIONS = [
    ("Status", ["backup_alter_tage"]),
    ("Einstellungen", ["backup_push_aktiv", "backup_bei_erfolg", "backup_max_alter_tage", "backup_ziel_person1", "backup_ziel_person2"]),
    ("Werkzeuge", ["backup_test", "backup_standardwerte"]),
]
