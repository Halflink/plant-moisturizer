import json as json


class JsonHandler:

    def __init__(self):

        with open("init.json") as jsonFile:
            init_info = json.load(jsonFile)
            jsonFile.close()
            self.debug_mode = init_info['Debug mode'].upper() == "YES"
            self.device_bus = init_info['Relay hat']['Device bus']
            hex_s = init_info['Relay hat']['Device Address']
            self.device_addr = int(hex_s, 16)
            self.pump_settings = init_info['Relay hat']['Pumps']
            self.log_path = init_info['Log path']
            self.max_log_lines = init_info['Max log lines']

    def print_settings(self):
        print("debug_mode: %s " % self.debug_mode)
        print("device_bus: %.1f " % self.device_bus)
        print("device_addr: " + hex(self.device_addr))
        no_of_pumps = len(self.pump_settings    )
        for element in range(no_of_pumps):
            print("Pump ID: %.1f " % self.pump_settings[element]['ID'])
            print("Pump time: %.1f " % self.pump_settings[element]['Pump time'])
        print("Log path: %s " % self.log_path)
        print("Max log lines: %.1f " % self.max_log_lines)


if __name__ == '__main__':
    jsonHandler = JsonHandler()
    jsonHandler.print_settings()
