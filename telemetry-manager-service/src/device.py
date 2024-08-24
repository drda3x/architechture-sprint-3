

__all__ = [
    "Device",
    "LightDevice",
    "HitDevice",
    "GateDevice",
    "VideoDevice"
]

class Device:
    def __init__(self, device_id):
        self.__id = device_id

    @property
    def id(self):
        return self.__id

    def get_data(self):
        pass


class LightDevice(Device):
    def get_data(self):
        return {
            "device_id": self.id,
            "status": "on"
        }

class HitDevice(Device):
    def get_data(self):
        return {
            "device_id": self.id,
            "temperature_val": 0.0
        }


class GateDevice(Device):
    def get_data(self):
        return {
            "device_id": self.id,
            "status": "open"
        }


class VideoDevice(Device):
    def get_data(self):
        return {
            "device_id": self.id,
            "status": "recording"
        }
