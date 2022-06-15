class MCP3008:
    # Class for MCP3008 ADC

    from spidev import SpiDev
    from datetime import datetime

    def __init__(self, bus=0, device=0):
        self.bus, self.device = bus, device
        self.spi = self.SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000  # 1MHz

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
        value = (self.read(channel=0) / 1023.0 * 3.3)
        return value

    def close(self):
        self.spi.close()

    def get_sensor_timestamp(self):

        now = self.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        sensor = [current_time, self.read_sensor(channel=0), self.read_sensor(channel=1), self.read_sensor(channel=2)]
        return sensor


if __name__ == '__main__':
    import sys
    import time

    mcp3008 = MCP3008()
    while True:
        try:
            volts = mcp3008.get_sensor_timestamp()
            print(volts)
            time.sleep(1)
        except KeyboardInterrupt as e:
            print("Quit the Loop")
            sys.exit()
