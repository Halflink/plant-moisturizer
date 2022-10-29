import json as json


class JsonHandler:

    def __init__(self):

        with open("./init.json") as jsonFile:
            init_info = json.load(jsonFile)
            jsonFile.close()
            self.device_bus = init_info['Relay hat']['Device bus']
            hex_s = init_info['Relay hat']['Device Address']
            self.device_addr = int(hex_s, 16)
            self.pump_settings = init_info['Relay hat']['Pumps']
            self.log_path = init_info['Logging']['Log path']
            self.log_level = init_info['Logging']['Log level']
            self.humidity_sensor_gpio = init_info['Humidity Sensor GPIO']
            self.web_port_number = init_info['Web port number']
            self.spi_bus = init_info['SPI']['Device Bus']
            self.spi_device = init_info['SPI']['Device']
            self.spi_readout_history_length = init_info['SPI']['Readout history length']
            self.spi_readout_interval = init_info['SPI']['Readout interval']
            self.rgb_led_gpio = init_info['RGB LED GPIO']

    def print_settings(self):
        print("device_bus: %.1f " % self.device_bus)
        print("device_addr: " + hex(self.device_addr))
        no_of_pumps = len(self.pump_settings)
        for element in range(no_of_pumps):
            print("Pump ID: %.1f " % self.pump_settings[element]['ID'])
            print("Pump time: %.1f " % self.pump_settings[element]['Pump time'])
            print("Sprinkling interval: %.1f " % self.pump_settings[element]['Sprinkler interval'])
            print("Sensor: %.1f " % self.pump_settings[element]['Sensor'])
            print("Sensor threshold: %.1f " % self.pump_settings[element]['Sensor threshold'])
        print("Log path: %s " % self.log_path)
        print("Log level: %.0f " % self.log_level)
        print("Humidity Sensor GPIO: %.0f" % self.humidity_sensor_gpio)
        print("Web port number: %.0f" % self.web_port_number)
        print("SPI Device Bus: %.0f" % self.spi_bus)
        print("SPI Device: %.0f" % self.spi_device)
        print("SPI Readout history length: %.0f" % self.spi_readout_history_length)
        for element in range(3):
            print("RGB LED GPIO: %0.f" % self.rgb_led_gpio[element])


if __name__ == '__main__':
    jsonHandler = JsonHandler()
    jsonHandler.print_settings()
