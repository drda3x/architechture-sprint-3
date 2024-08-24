import device


device_type_map = dict(
    light_device=device.LightDevice,
    hit_device=device.HitDevice,
    gate_device=device.GateDevice,
    video_device=device.VideoDevice
)


class DeviceDatabase:
    def __init__(self):
        self.__db = {}

    def add(self, device_data):
        device_type = device_type_map.get(device_data['device_type'])
        if device_type:
            if not device_data['device_id'] in self.__db:
                self.__db[device_data['device_id']] = device_type(device_data['device_id'])
                print(f"Add device {device_data['device_id']}")

    def get(self, device_data):
        return self.__db.get(device_data['device_id'])
