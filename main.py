class MainClass:
    # Import
    import sys
    from HumiditySensor import HumiditySensor
    from JsonHandler import JsonHandler
    from Pumps import Pumps
    from MoistureSensor import MoistureSensor
    from Logger import Logger
    import logging
    import threading
    import time

    # Variables

    def __init__(self):

        # Get settings
        json_handler = self.JsonHandler()

        # Initialize logging. The logger class is only there to initialize pythons logging module
        self.log_name = 'MoisturizerLogging'
        self.logger = self.Logger(log_level=json_handler.log_level,
                                  log_name=self.log_name,
                                  log_folder=json_handler.log_path)
        self.log = self.logging.getLogger(self.log_name)

        # Set pumps (relais hat)
        self.pumps = self.Pumps(device_addr=json_handler.device_addr,
                                device_bus=json_handler.device_bus,
                                pump_settings=json_handler.pump_settings,
                                log_name=self.log_name)

        # Set Sensors in own thread
        self.moistureSensors = self.MoistureSensor(log_name=self.log_name, bus=json_handler.spi_bus,
                                                   device=json_handler.spi_device,
                                                   readout_history_length=json_handler.spi_readout_history_length)
        self.humiditySensor = self.HumiditySensor(log_name=self.log_name, dht_pin=json_handler.humidity_sensor_gpio)
        self.sensor_thread = self.threading.Thread(target=self.sensor_thread_function, args=("sensor thread",))

        # Set web port number
        self.web_port_number = json_handler.web_port_number

    def activate_pump(self, pump_index):
        if 0 <= pump_index < self.pumps.length():
            self.pumps.water_plants(pump_index)

    def pump_test(self):
        while True:
            try:
                for i in range(self.pumps.length()):
                    self.log.info('Pump = %.1f ' % i)
                    self.pumps.water_plants(i)
                    print(self.moistureSensors.get_last_read_out_string())
            except KeyboardInterrupt as e:
                print('Quit the Loop')
                self.sys.exit()

    def sensor_thread_function(self, thread_name):
        self.log.debug('Initializing ' + thread_name)
        try:
            while True:
                self.moistureSensors.write_sensor_read_out()
                self.humiditySensor.write_sensor_read_out()
                self.time.sleep(10)
        except KeyboardInterrupt as e:
            self.log.debug('Sensor thread keyboard interruption')
            self.moistureSensors.close()

    def start_sensor_thread(self):
        self.sensor_thread.start()


if __name__ == '__main__':
    # If main is started, it will test the sensors and the pumps.
    mainClass = MainClass()
    mainClass.start_sensor_thread()
    mainClass.pump_test()
