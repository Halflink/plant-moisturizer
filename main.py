import threading


class MainClass:
    # Import
    import sys
    from JsonHandler import JsonHandler
    from Pumps import Pumps
    from MCP3008 import MCP3008
    from Log import Log
    import threading
    import time

    # Variables

    def __init__(self):

        json_handler = self.JsonHandler()
        self.debug_mode = json_handler.debug_mode
        device_bus = json_handler.device_bus
        device_addr = json_handler.device_addr
        pump_settings = json_handler.pump_settings
        log_path = json_handler.log_path
        max_log_lines = json_handler.max_log_lines
        self.pumps = self.Pumps(device_addr, device_bus, pump_settings, self.debug_mode)
        self.log = self.Log(log_path, max_log_lines)
        self.sensors = self.MCP3008(self.log)
        self.sensor_thread = self.threading.Thread(target=self.sensor_thread_function, args=("sensor thread",))

    def activate_pump(self, pump_index):
        if 0 <= pump_index < self.pumps.length():
            self.pumps.water_plants(pump_index)

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

    def sensor_thread_function(self, thread_name):
        self.log.add_line("main", "Initializing sensor thread")
        try:
            while True:
                self.sensors.set_read_outs()
                self.time.sleep(10)
        except KeyboardInterrupt as e:
            self.log.add_line("sensor thread", "keyboard interruption")
            self.sensors.close()

    def start_sensor_thread(self):
        self.sensor_thread.start()


if __name__ == '__main__':
    mainClass = MainClass()
    mainClass.start_sensor_thread()
    mainClass.pump_test()
