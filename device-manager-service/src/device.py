

__all__ = [
    "Device",
    "LightDevice",
    "HitDevice",
    "GateDevice",
    "VideoDevice"
]

class Device:
    def __init__(self, device_id, logger):
        self.__id = device_id
        self.__logger = logger

    @property
    def id(self):
        return self.__id

    @property
    def logger(self):
        return self.__logger

    def set_state(self, nes_state, *args, **kwargs):
        pass


class LightDevice(Device):
    def set_state(self, new_state, *args, **kwargs):
        self.logger.info(f"Set light to {new_state}")


class HitDevice(Device):
    def set_state(self, new_state, *args, **kwargs):
        self.logger.info(f"Set hit device state to {new_state}")


class GateDevice(Device):
    def set_state(self, new_state, *args, **kwargs):
        self.logger.info(f"Set Gate device to {new_state}")


class VideoDevice(Device):
    def set_state(self, new_state, *args, **kwargs):
        self.logger.info(f"Set VideoDevice to {new_state}")
