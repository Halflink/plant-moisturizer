class MCP3008:
    # Class for MCP3008 ADC

    from spidev import SpiDev

    # Variables
    read_outs = []

    def __init__(self, log, bus=0, device=0, readout_history_length=10):
        self.bus, self.device, self.readout_history_length = bus, device, readout_history_length
        self.spi = self.SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000  # 1MHz
        self.log = log

    def close(self):
        self.spi.close()

    def get_last_read_out_string(self):
        return self.convert_float_list_to_string(self.read_outs[-1])

    def get_sensor_data(self):
        """
        Get a timestamp and a readout from all sensors. Return them as an array
        """
        sensor = [self.read_sensor(channel=0), self.read_sensor(channel=1), self.read_sensor(channel=2)]
        return sensor

    @staticmethod
    def convert_float_list_to_string(read_out):
        read_out_string = ''
        print(len(read_out))
        for i in range(len(read_out)):
            print(i)
            if read_out_string != '':
                read_out_string = read_out_string + ' | '
            read_out_string = read_out_string + str(round(read_out[i], 2))
        return read_out_string

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

    def set_read_outs(self):
        """
        Read out all sensors and write them to file
        Also keep last 10 readouts in memory
        """
        sensor_readout = self.get_sensor_data()
        self.read_outs.append(sensor_readout)
        self.log.add_line('Moisture read-out', ' | ' + self.convert_float_list_to_string(sensor_readout))
        if len(self.read_outs) > self.readout_history_length:
            self.read_outs.pop(0)


if __name__ == '__main__':
    import sys
    import time
    from Log import Log

    log = Log()
    mcp3008 = MCP3008(log)
    while True:
        try:
            mcp3008.set_read_outs()
            print(mcp3008.get_last_read_out_string())
            time.sleep(1)
        except KeyboardInterrupt as e:
            print("Quit the Loop")
            sys.exit()
