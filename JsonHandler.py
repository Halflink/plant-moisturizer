import json as json


class JsonHandler:

    def __init__(self):

        with open("init.json") as jsonFile:
            init_info = json.load(jsonFile)
            jsonFile.close()
            self.device_bus = init_info['Relay hat']['Device bus']
            hex_s = init_info['Relay hat']['Device Address']
            self.device_addr = int(hex_s, 16)
            self.pump_settings = init_info['Relay hat']['Pumps']
            self.log_path = init_info['Log path']
            self.log_level = init_info['Log level']
            self.humidity_sensor_gpio = init_info['Humidity Sensor GPIO']
            self.web_port_number = init_info['Web port number']

    def print_settings(self):
        print("device_bus: %.1f " % self.device_bus)
        print("device_addr: " + hex(self.device_addr))
        no_of_pumps = len(self.pump_settings)
        for element in range(no_of_pumps):
            print("Pump ID: %.1f " % self.pump_settings[element]['ID'])
            print("Pump time: %.1f " % self.pump_settings[element]['Pump time'])
        print("Log path: %s " % self.log_path)
        print("Log level: %.0f " % self.log_level)
        print("Humidity Sensor GPIO: %.0f" % self.humidity_sensor_gpio)
        print("Web port number: %.0f" % self.web_port_number)


if __name__ == '__main__':
    jsonHandler = JsonHandler()
    jsonHandler.print_settings()
