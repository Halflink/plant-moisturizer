import logging


class Pumps:
    import smbus
    import logging

    class Pump:

        # Import
        import time as time
        import logging

        def __init__(self, bus, pump_id, pump_time, device_addr, log_name):

            self.log = self.logging.getLogger(log_name)
            self.device_addr = device_addr
            self.pump_id = pump_id
            self.pump_time = pump_time
            self.bus = bus

        def start_pump(self):
            self.log.debug('Start pump = %.1f ' % self.pump_id)
            self.bus.write_byte_data(self.device_addr, self.pump_id, 0xFF)

        def stop_pump(self):
            self.log.debug('Stop pump = %.1f ' % self.pump_id)
            self.bus.write_byte_data(self.device_addr, self.pump_id, 0x00)

        def water_plants(self):
            self.start_pump()
            self.time.sleep(self.pump_time)
            self.stop_pump()

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
                             log_name=log_name)
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
