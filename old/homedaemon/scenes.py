from threading import Thread, Event, RLock
from datetime import datetime
from time import sleep
from homedaemon.bus import Bus
from homedaemon.logger import Logger
from homedaemon.devices import Devices
from typing import Dict, Any, List, Set, Callable
from pyiot.software import Time


class SceneInterface:
    def __init__(self, sid: str):
        self.sid = sid
        self.bus = Bus()
        self.devices = Devices()
        self.logger = Logger()
        self.name = ""
        self.model = ""
        self.place = ""
        self.running: Set[Callable[[], None]] = set()
        self.lock = RLock()

    def _runner(self, handler: Callable[[], None], *args: Any) -> None:
        with self.lock:
            self.logger.debug(
                f"Scene {self.name} running list {self.running} {handler}"
            )
            if handler in self.running:
                self.logger.warning(
                    f"Scene {self.name}: {handler.__name__} already started"
                )
                return
            else:
                self.running.add(handler)
            self.bus.emit(
                f"report.{self.sid}.status.on",
                {
                    "cmd": "report",
                    "sid": self.sid,
                    "data": {
                        "name": self.name,
                        "status": "run",
                        "handler": handler.__name__,
                    },
                },
            )

            try:
                handler()
            except Exception as err:
                self.logger.error(f"scene running error {self.name} {err}")
            finally:
                self.bus.emit(
                    f"report.{self.sid}.status.off",
                    {
                        "cmd": "report",
                        "sid": self.sid,
                        "data": {
                            "name": self.name,
                            "status": "stop",
                            "handler": handler.__name__,
                        },
                    },
                )
                self.running.remove(handler)

    def sleep(self, s: int):
        sleep(s)

    def get_device(self, sid: str):
        return self.devices.get(sid)

    def store_device_state(self, *sids: str):
        pass

    def restore_devices_state(self, *sids: str):
        pass

    def device_status(self) -> Dict[str, Any]:
        ret = {"status": "off", "sid": self.sid, "name": self.name, "place": self.place}
        if self.running:
            events: List[str] = [x.__name__ for x in self.running]
            ret["status"] = "on"
            ret["events"] = events
        return ret

    def now(self):
        """Retrun time now"""
        return datetime.now().time()


class BaseScene(SceneInterface):
    def __init__(self, sid: str):
        super().__init__(sid)
        self.reversible = False
        self.model = "scene"
        self.bus.add_trigger(f"write.{self.sid}.status.on", self._on, self.on)
        self.bus.add_trigger(f"write.{self.sid}.status.off", self._off, self.off)

    def _on(self):
        if self.on in self.running:
            self.logger.warning(f"Scene {self.name} already started")
        else:
            self.running.add(self.on)
        self.bus.emit(
            f"report.{self.sid}.status.on",
            {
                "cmd": "report",
                "sid": self.sid,
                "data": {"status": "run", "name": self.name},
            },
        )
        try:
            self.on()
        except Exception as err:
            self.logger.error(f"scene running error {self.name} {err}")
        finally:
            if not self.reversible:
                self.bus.emit(
                    f"report.{self.sid}.status.off",
                    {
                        "cmd": "report",
                        "sid": self.sid,
                        "data": {"status": "end", "name": self.name},
                    },
                )

    def on(self):
        pass

    def _off(self):
        if not self.reversible or self.on not in self.running:
            return
        try:
            self.off()
        except Exception as err:
            self.logger.error(f"scene running error {self.name} {err}")
        finally:
            self.bus.emit(
                f"report.{self.sid}.status.off",
                {
                    "cmd": "report",
                    "sid": self.sid,
                    "data": {"status": "end", "name": self.name},
                },
            )

    def off(self):
        pass


class BaseAutomation(SceneInterface):
    def __init__(self, sid: str):
        super().__init__(sid)
        self.model = "automation"

    def add_trigger(self, trigger: str, handler: Callable[[], None]) -> None:
        self.bus.add_trigger(trigger, self._runner, handler)


class RunAfter:
    def __init__(self, delay: int, callback: Callable[[], None], *args: Any):
        self.delay = delay
        self.callback = callback
        self.args = args
        self.ev = Event()
        self._is_waiting = False

    def wait(self):
        Thread(target=self._wait, daemon=True).start()

    def _wait(self):
        self.ev.clear()
        self._is_waiting = True
        if not self.ev.wait(timeout=self.delay):
            if self.args:
                self.callback(*self.args)
            else:
                self.callback()
        else:
            print("canceled")

    @property
    def is_waiting(self):
        return self._is_waiting

    def cancel(self):
        self.ev.set()
        self._is_waiting = False


class TimeRange:
    """TimeRange"""

    def __init__(self, _from: Time, _to: Time):
        self._from = _from
        self._to = _to

    def __contains__(self, value: Time):
        if value > self._to:
            return self._from <= value >= self._to
        elif value < self._to:
            return self._from >= value <= self._to
