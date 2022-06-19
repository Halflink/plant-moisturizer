class MCP3008:
    # Class for MCP3008 ADC

    from spidev import SpiDev
    from datetime import datetime

    # Variables
    read_outs = []

    def __init__(self, log, bus=0, device=0, readout_history_length=10):
        self.bus, self.device, self.readout_history_length = bus, device, readout_history_length
        self.spi = self.SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000  # 1MHz
        self.log = log

    def open(self):
        # connect spi object to spi device
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000  # 1MHz

    def read(self, channel=0):
        """
        read SPI data from MCP3008 on channel -> digital value
            spi.xfer2() send three bytes to the device
                the first byte is 1 -> 00000001
                the second byte is 8 + channel and left shift with 4 bits
                the third byte is 0 -> 00000000
            the device return 3 bytes as response
        """
        # perform spi transaction
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        # extract value from data bytes
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def read_sensor(self, channel=0):
        """
        read the digital data from MCP3008 and convert it to voltage
            MCP3008: 10bit ADC -> value in number range 0-1023
            spi value -> voltage
                   0  ->  0v
                1023  ->  vmax
        """
        value = (self.read(channel) / 1023.0 * 3.3)
        return value

    def close(self):
        self.spi.close()

    def get_sensor_readout(self):
        """
        Get a timestamp and a readout from all sensors. Return them as an array
        """
        now = self.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        sensor = [current_time, self.read_sensor(channel=0), self.read_sensor(channel=1), self.read_sensor(channel=2)]
        return sensor

    def set_readouts(self):
        """
        Read out all sensors and write them to file
        Also keep last 10 readouts in memory
        """
        sensor_readout = self.get_sensor_readout()
        self.read_outs.append(sensor_readout)
        self.log.add_line(" / ".join(sensor_readout))
        if len(self.read_outs) > self.readout_history_length:
            self.read_outs.pop(0)


if __name__ == '__main__':
    import sys
    import time

    mcp3008 = MCP3008()
    while True:
        try:
            volts = mcp3008.get_sensor_readout()
            print(volts)
            time.sleep(1)
        except KeyboardInterrupt as e:
            print("Quit the Loop")
            sys.exit()
