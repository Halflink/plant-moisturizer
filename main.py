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

    class PowerLed:

        def __init__(self, GPIO, led_gpio):
            self.GPIO = GPIO
            self.red_gpio = led_gpio[0]
            self.green_gpio = led_gpio[1]
            self.blue_gpio = led_gpio[2]
            self.GPIO.setmode(GPIO.BCM)
            self.GPIO.setup(self.red_gpio, self.GPIO.OUT)
            self.GPIO.setup(self.green_gpio, self.GPIO.OUT)
            self.GPIO.setup(self.blue_gpio, self.GPIO.OUT)

        def led_off(self):
            rgb = [False, False, False]
            self.led_set(rgb)

        def led_set(self, rgb):
            if rgb is not None:
                if rgb[0]:
                    self.GPIO.output(self.red_gpio, self.GPIO.LOW)
                else:
                    self.GPIO.output(self.red_gpio, self.GPIO.HIGH)

                if rgb[1]:
                    self.GPIO.output(self.green_gpio, self.GPIO.LOW)
                else:
                    self.GPIO.output(self.green_gpio, self.GPIO.HIGH)

                if rgb[2]:
                    self.GPIO.output(self.blue_gpio, self.GPIO.LOW)
                else:
                    self.GPIO.output(self.blue_gpio, self.GPIO.HIGH)

        def led_on(self, colour):
            rgb = None
            if colour == 'RED':
                rgb = [True, False, False]
            elif colour == 'GREEN':
                rgb = [False, True, False]
            elif colour == 'BLUE':
                rgb = [False, False, True]
            elif colour == 'CYAN':
                rgb = [False, True, True]
            elif colour == 'MAGNENTA':
                rgb = [True, False, True]
            elif colour == 'YELLOW':
                rgb = [True, True, False]
            else:
                rgb = [False, False, False]
            self.led_set(rgb)

    def __init__(self):

        # Get settings
        json_handler = self.JsonHandler()

        # Set power LED
        self.powerLed = self.PowerLed(self.GPIO, json_handler.rgb_led_gpio)

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
        self.readout_interval = json_handler.spi_readout_interval

        # Set web port number
        self.web_port_number = json_handler.web_port_number

    def power_led_program_running(self):
        self.powerLed.led_on("GREEN")

    def deactivate_power_led(self):
        self.powerLed.led_off()

    def cleanup_gpio(self):
        self.GPIO.cleanup()

    def activate_pump(self, pump_index):
        if 0 <= pump_index < self.relayHat.length():
            self.relayHat.water_plants(pump_index)

    def check_time_difference(self, time_stamp_1, time_stamp_2, interval):
        if time_stamp_1 is None or time_stamp_2 is None:
            return True
        else:
            time_stamp = time_stamp_1 + self.datetime.timedelta(seconds=interval)
            return time_stamp < time_stamp_2

    def check_sprinkler(self):
        for pump in self.relayHat.pumps:
            readout_sensor = self.moistureSensors.get_last_readout(pump.sensor)
            pump_sensor_threshold = pump.sensor_threshold
            self.log.debug('check_sprinkler: Iterating pumps: pump {} , readout is {}, threshold is {}'.format(
                pump.pump_id, readout_sensor, pump_sensor_threshold))
            if readout_sensor <= pump_sensor_threshold:
                if self.check_time_difference(pump.last_run_datetime, self.datetime.datetime.now(),
                                              pump.sprinkler_interval):
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

    def sensor_thread_function(self, thread_name, stop_thread_event, ):
        self.log.debug('Initializing ' + thread_name)
        last_readout_datetime = None
        try:
            while True:
                current_datetime = self.datetime.datetime.now()
                if self.check_time_difference(last_readout_datetime, current_datetime,
                                              self.readout_interval):
                    last_readout_datetime = current_datetime
                    self.moistureSensors.write_sensor_read_out()
                    self.humiditySensor.write_sensor_read_out()
                if self.auto_sprinkling:
                    self.check_sprinkler()
                if stop_thread_event.is_set():
                    self.log.debug('sensor_thread_function: Sensor thread is stopped')
                    break
        except KeyboardInterrupt as e:
            self.log.debug('Sensor thread keyboard interruption')
            self.moistureSensors.close()
        except Exception as e:
            self.powerLed.led_set("RED")
            self.log.exception("Error occurred in sensor thread")

    def start_sensor_thread(self):
        self.sensor_thread.start()

    def end_sensor_thread(self):
        self.powerLed.led_on('BLUE')
        self.stop_thread_event.set()
        print('Wait for tread to stop...')
        self.sensor_thread.join()


if __name__ == '__main__':
    # If main is started, it will test the sensors and the pumps.
    mainClass = MainClass()
    mainClass.start_sensor_thread()
    mainClass.pump_test()
