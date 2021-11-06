class Pumps:
    import smbus

    class Pump:

        # Import
        import time as time

        def __init__(self, bus, pump_id, pump_time, device_addr, debug_mode):

            self.device_addr = device_addr
            self.debug_mode = debug_mode
            self.pump_id = pump_id
            self.pump_time = pump_time
            self.bus = bus

        def start_pump(self):
            if self.debug_mode:
                print("Start pump = %.1f " % self.pump_id)
            self.bus.write_byte_data(self.device_addr, self.pump_id, 0xFF)

        def stop_pump(self):
            if self.debug_mode:
                print("Stop pump = %.1f " % self.pump_id)
            self.bus.write_byte_data(self.device_addr, self.pump_id, 0x00)

        def water_plants(self):
            self.start_pump()
            self.time.sleep(self.pump_time)
            self.stop_pump()

    def __init__(self, device_addr, device_bus, pump_settings, debug_mode):

        self.bus = self.smbus.SMBus(device_bus)
        self.pumps = []

        no_of_pumps = len(pump_settings)
        for element in range(no_of_pumps):
            if debug_mode:
                print("Pump ID: %.1f " % pump_settings[element]['ID'])
                print("Pump time: %.1f " % pump_settings[element]['Pump time'])
            pump = self.Pump(self.bus,
                             pump_settings[element]['ID'],
                             pump_settings[element]['Pump time'],
                             device_addr,
                             debug_mode)
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
