"""Backup-Meldungen: Fachlogik (Port von backup_benachrichtigung.yaml)."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import Event
from homeassistant.util import dt as dt_util

from .const import DOMAIN, alter_tage, letztes_text
from .framework import LogicBase

_LOGGER = logging.getLogger(__name__)
URL = "/config/backup/overview"


class Logic(LogicBase):
    def __init__(self, rt) -> None:
        super().__init__(rt)
        rt.actions.update(test=self._test, reset=self._reset)

    async def _reset(self) -> None:
        self.rt.reset_defaults()

    async def async_start(self) -> None:
        rt = self.rt
        rt.track_state([rt.cfg("event_entity")], self._ereignis)
        rt.track_state([rt.cfg("last_success")], rt.refresh)
        rt.track_time(self._ueberfaellig, hour=9, minute=0, second=0)
        rt.track_interval(rt.refresh, timedelta(hours=1))

    async def melden(self, titel: str, nachricht: str, stufe: str = "active") -> None:
        rt = self.rt
        await rt.pn_create(titel, nachricht, "backup_meldung")
        await rt.notify(
            titel,
            nachricht,
            {"tag": "backup", "url": URL, "push": {"interruption-level": stufe}},
        )

    async def _test(self) -> None:
        await self.melden(
            "💾 Test: Backup-Meldung",
            f"So sieht eine Meldung aus. Letztes erfolgreiches Backup: {letztes_text(self.rt)}.",
        )

    async def _ereignis(self, event: Event) -> None:
        rt = self.rt
        old, new = event.data.get("old_state"), event.data.get("new_state")
        if new is None or not rt.on("backup_push_aktiv"):
            return
        if old is not None and old.state in ("unavailable", "unknown"):
            return
        typ = new.attributes.get("event_type")
        if typ == "failed":
            grund = new.attributes.get("failed_reason")
            await self.melden(
                "⚠️ Backup fehlgeschlagen",
                f"Das automatische Backup ist fehlgeschlagen{': ' + str(grund) if grund else ''}. "
                "Bitte unter Einstellungen → System → Backups prüfen.",
                "time-sensitive",
            )
        elif typ == "completed" and rt.on("backup_bei_erfolg"):
            mb = int(round(rt.num(rt.cfg("size_entity"), 0) or 0))
            await self.melden("💾 Backup fertig", f"Das automatische Backup wurde erfolgreich erstellt ({mb} MB).")

    async def _ueberfaellig(self, _now) -> None:
        rt = self.rt
        if not rt.on("backup_push_aktiv"):
            return
        alter = alter_tage(rt)
        if alter is None or alter <= rt.flt("backup_max_alter_tage", 9):
            return
        ts = dt_util.parse_datetime(rt.state(rt.cfg("last_success")) or "")
        datum = dt_util.as_local(ts).strftime("%d.%m.%Y") if ts else "unbekannt"
        await self.melden(
            "⚠️ Backup überfällig",
            f"Das letzte erfolgreiche Backup ist vom {datum}. Bitte den Backup-Zeitplan prüfen.",
            "time-sensitive",
        )
