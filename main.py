class MainClass:

    # Import
    import sys
    from JsonHandler import JsonHandler
    from Pumps import Pumps

    # Variables

    def __init__(self):

        json_handler = self.JsonHandler()
        self.debug_mode = json_handler.debug_mode
        device_bus = json_handler.device_bus
        device_addr = json_handler.device_addr
        pump_settings = json_handler.pump_settings
        self.pumps = self.Pumps(device_addr, device_bus, pump_settings, self.debug_mode)

    def pump_test(self):
        while True:
            try:
                for i in range(self.pumps.length()):
                    if self.debug_mode:
                        print("Pump = %.1f " % i)
                    self.pumps.water_plants(i)
            except KeyboardInterrupt as e:
                print("Quit the Loop")
                self.sys.exit()


if __name__ == '__main__':
    mainClass = MainClass()
    mainClass.pump_test()

