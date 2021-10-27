import json as json


class JsonHandler:

    def __init__(self):

        with open("init.json") as jsonFile:
            init_info = json.load(jsonFile)
            jsonFile.close()

            self.device_bus = init_info['Relay hat']['Device bus']
            hex_s = init_info['Relay hat']['Device Address']
            self.device_addr = int(hex_s, 16)
            self.pump_a = init_info['Pumps']['Pump a']
            self.pump_b = init_info['Pumps']['Pump b']
            self.pump_c = init_info['Pumps']['Pump c']
            self.pump_d = init_info['Pumps']['Pump d']
            self.pump_time = init_info['Pumps']['Pump time']

    def print_settings(self):
        print("device_bus: %.1f " % self.device_bus)
        print("device_addr: " + self.device_addr)
        print("pump_a: %.1f " % self.pump_a)
        print("pump_b: %.1f " % self.pump_b)
        print("pump_c: %.1f " % self.pump_c)
        print("pump_d: %.1f " % self.pump_d)
        print("pump_time: %.1f " % self.pump_time)


if __name__ == '__main__':
    jsonHandler = JsonHandler()
    jsonHandler.print_settings()
