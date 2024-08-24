

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

    def set_state(self, nes_state, *args, **kwargs):
        pass


class LightDevice(Device):
    def set_state(self, new_state, *args, **kwargs):
        print(f"Set light to {new_state}")


class HitDevice(Device):
    def set_state(self, new_state, *args, **kwargs):
        print(f"Set hit device state to {new_state}")


class GateDevice(Device):
    def set_state(self, new_state, *args, **kwargs):
        print(f"Set Gate device to {new_state}")


class VideoDevice(Device):
    def set_state(self, new_state, *args, **kwargs):
        print(f"Set VideoDevice to {new_state}")
