import logging


class Pumps:
    import smbus
    import logging

    class Pump:

        # Import
        import time as time
        from datetime import datetime as datetime
        import logging

        last_run_datetime = None

        def __init__(self, bus, pump_id, pump_time, device_addr, log_name, sprinkler_interval, sensor
                     , sensor_threshold):

            self.log = self.logging.getLogger(log_name)
            self.device_addr = device_addr
            self.pump_id = pump_id
            self.pump_time = pump_time
            self.bus = bus
            self.sprinkler_interval = sprinkler_interval
            self.sensor = sensor
            self.sensor_threshold = sensor_threshold

        def start_pump(self):
            self.log.info('Start pump %.1f ' % self.pump_id)
            self.bus.write_byte_data(self.device_addr, self.pump_id, 0xFF)

        def stop_pump(self):
            self.log.debug('Stop pump %.1f ' % self.pump_id)
            self.bus.write_byte_data(self.device_addr, self.pump_id, 0x00)

        def water_plants(self):
            if self.last_run_datetime is not None:
                last_run = self.last_run_datetime.strftime("%d-%m-%Y, %H:%M:%S")
                self.log.info('Last run pump {} is at {}'.format(self.pump_id, last_run))
            self.start_pump()
            self.time.sleep(self.pump_time)
            self.stop_pump()
            self.last_run_datetime = self.datetime.now()

    def __init__(self, device_addr, device_bus, pump_settings, log_name):

        self.log = self.logging.getLogger(log_name)
        self.bus = self.smbus.SMBus(device_bus)
        self.pumps = []

        no_of_pumps = len(pump_settings)
        for element in range(no_of_pumps):
            self.log.debug('Pump ID: %.1f ' % pump_settings[element]['ID'])
            self.log.debug('Pump time: %.1f ' % pump_settings[element]['Pump time'])
            pump = self.Pump(bus=self.bus,
                             pump_id=pump_settings[element]['ID'],
                             pump_time=pump_settings[element]['Pump time'],
                             device_addr=device_addr,
                             log_name=log_name,
                             sprinkler_interval=pump_settings[element]['Sprinkler interval'],
                             sensor=pump_settings[element]['Sensor'],
                             sensor_threshold=pump_settings[element]['Sensor threshold'])
            self.pumps.append(pump)

    def length(self):
        length = len(self.pumps)
        return length

    def get_pump(self, pump_no):
        pump = self.pumps[pump_no]
        return pump

    def water_plants(self, pump_no):
        pump = self.get_pump(pump_no)
        if pump is not None:
            pump.water_plants()
