class MainClass:
    # Import
    import sys
    from JsonHandler import JsonHandler
    from Pumps import Pumps
    from MCP3008 import MCP3008
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
        self.sensors = self.MCP3008(log_name=self.log_name)
        self.sensor_thread = self.threading.Thread(target=self.sensor_thread_function, args=("sensor thread",))

    def activate_pump(self, pump_index):
        if 0 <= pump_index < self.pumps.length():
            self.pumps.water_plants(pump_index)

    def pump_test(self):
        while True:
            try:
                for i in range(self.pumps.length()):
                    self.log.info('Pump = %.1f ' % i)
                    self.pumps.water_plants(i)
            except KeyboardInterrupt as e:
                print('Quit the Loop')
                self.sys.exit()

    def sensor_thread_function(self, thread_name):
        self.log.debug('Initializing ' + thread_name)
        try:
            while True:
                self.sensors.set_read_outs()
                self.time.sleep(10)
        except KeyboardInterrupt as e:
            self.log.debug('Sensor thread keyboard interruption')
            self.sensors.close()

    def start_sensor_thread(self):
        self.sensor_thread.start()


if __name__ == '__main__':
    # If main is started, it will test the sensors and the pumps.
    mainClass = MainClass()
    mainClass.start_sensor_thread()
    mainClass.pump_test()
