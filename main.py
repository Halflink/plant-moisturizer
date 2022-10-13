import time


class MainClass:
    # Import
    import sys
    from HumiditySensor import HumiditySensor
    from JsonHandler import JsonHandler
    from RelayHat import RelayHat
    from MoistureSensor import MoistureSensor
    from Logger import Logger
    import logging
    import threading
    import time as time
    import datetime as datetime
    import RPi.GPIO as GPIO

    # Variables
    stop_thread_event = threading.Event()
    auto_sprinkling = False

    def __init__(self):

        # Get settings
        json_handler = self.JsonHandler()

        # Set power LED
        self.power_led_gpio = json_handler.power_led_gpio
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setup(self.power_led_gpio, self.GPIO.OUT)

        # Initialize logging. The logger class is only there to initialize pythons logging module
        self.log_name = 'MoisturizerLogging'
        self.logger = self.Logger(log_level=json_handler.log_level,
                                  log_name=self.log_name,
                                  log_folder=json_handler.log_path)
        self.log = self.logging.getLogger(self.log_name)

        # Set pumps (relais hat)
        self.relayHat = self.RelayHat(device_addr=json_handler.device_addr,
                                      device_bus=json_handler.device_bus,
                                      pump_settings=json_handler.pump_settings,
                                      log_name=self.log_name)

        # Set Sensors in own thread
        self.moistureSensors = self.MoistureSensor(log_name=self.log_name, bus=json_handler.spi_bus,
                                                   device=json_handler.spi_device,
                                                   readout_history_length=json_handler.spi_readout_history_length)
        self.humiditySensor = self.HumiditySensor(log_name=self.log_name, dht_pin=json_handler.humidity_sensor_gpio)
        self.sensor_thread = self.threading.Thread(target=self.sensor_thread_function, args=("sensor thread",
                                                                                             self.stop_thread_event))

        # Set web port number
        self.web_port_number = json_handler.web_port_number

    def activate_power_led(self):
        self.GPIO.output(self.power_led_gpio, self.GPIO.HIGH)

    def deactivate_power_led(self):
        self.GPIO.output(self.power_led_gpio, self.GPIO.LOW)

    def cleanup_gpio(self):
        self.GPIO.cleanup()

    def activate_pump(self, pump_index):
        if 0 <= pump_index < self.relayHat.length():
            self.relayHat.water_plants(pump_index)

    def check_sprinkler(self):
        for pump in self.relayHat.pumps:
            readout_sensor = self.moistureSensors.get_last_readout(pump.sensor)
            pump_sensor_threshold = pump.sensor_threshold
            self.log.debug('check_sprinkler: Iterating pumps: pump {} , readout is {}, threshold is {}'.format(
                pump.pump_id, readout_sensor, pump_sensor_threshold))
            if readout_sensor <= pump_sensor_threshold:
                self.log.debug('check_sprinkler: check last run')
                if pump.last_run_datetime is None:
                    self.log.debug('check_sprinkler: last run was none')
                    pump.water_plants()
                else:
                    next_run = pump.last_run_datetime + self.datetime.timedelta(seconds=pump.sprinkler_interval)
                    current_datetime = self.datetime.datetime.now()
                    self.log.debug('check_sprinkler: next run at {}, current date time is {}'.format(next_run, current_datetime))
                    if current_datetime > next_run:
                        pump.water_plants()

    def pump_test(self):
        while True:
            try:
                for i in range(self.relayHat.length()):
                    self.log.info('Pump = %.1f ' % i)
                    self.relayHat.water_plants(i)
                    print(self.moistureSensors.get_last_read_out_string())
            except KeyboardInterrupt as e:
                print('Quit the Loop')
                self.sys.exit()

    def sensor_thread_function(self, thread_name, stop_thread_event,):
        self.log.debug('Initializing ' + thread_name)
        try:
            while True:
                self.moistureSensors.write_sensor_read_out()
                self.humiditySensor.write_sensor_read_out()
                time.sleep(10)
                if self.auto_sprinkling:
                    self.log.debug('sensor_thread_function: auto sprinkling is on, check sprinkler')
                    self.check_sprinkler()
                if stop_thread_event.is_set():
                    self.log.debug('sensor_thread_function: Sensor thread is stopped')
                    break
        except KeyboardInterrupt as e:
            self.log.debug('Sensor thread keyboard interruption')
            self.moistureSensors.close()

    def start_sensor_thread(self):
        self.sensor_thread.start()

    def end_sensor_thread(self):
        self.stop_thread_event.set()
        print('Wait for tread to stop...')
        self.sensor_thread.join()


if __name__ == '__main__':
    # If main is started, it will test the sensors and the pumps.
    mainClass = MainClass(4)
    mainClass.start_sensor_thread()
    mainClass.pump_test()
