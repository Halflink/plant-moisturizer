class MainClass:

    # Import
    import time as time
    import smbus
    import sys
    from JsonHandler import JsonHandler

    # Variables

    def __init__(self):

        self.json_handler = self.JsonHandler()
        self.device_bus = self.json_handler.device_bus
        self.device_addr = self.json_handler.device_addr
        self.bus = self.smbus.SMBus(self.device_bus)

    def relay_test(self):
        while True:
            try:
                for i in range(1, 5):
                    print("Relay = %.1f " % i)
                    self.bus.write_byte_data(self.device_addr, i, 0xFF)
                    self.time.sleep(2)
                    self.bus.write_byte_data(self.device_addr, i, 0x00)
                    self.time.sleep(2)
            except KeyboardInterrupt as e:
                print("Quit the Loop")
                self.sys.exit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mainClass = MainClass()
    mainClass.relay_test()

