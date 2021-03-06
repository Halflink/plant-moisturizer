class MCP3008:
    """
        Class for MCP3008 ADC
        Using the MCP3008 chip to rad out the sensors.

    """
    from spidev import SpiDev
    import logging
    import datetime

    # Variables
    read_outs = []
    time_read_outs = []

    def __init__(self, log_name='', bus=0, device=0, readout_history_length=10):
        self.bus, self.device, self.readout_history_length = bus, device, readout_history_length
        self.spi = self.SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000  # 1MHz
        self.log = self.logging.getLogger(log_name)

    def add_read_outs(self, read_out):
        # record read out and time of read out
        self.read_outs.append(read_out)
        if len(self.read_outs) > self.readout_history_length:
            self.read_outs.pop(0)  # keep only 10 readouts in the array
        self.time_read_outs.append(self.get_time_string)
        if len(self.time_read_outs) > self.readout_history_length:
            self.time_read_outs.pop(0) # keep only 10 readouts in the array

    def close(self):
        self.spi.close()

    @staticmethod
    def convert_float_list_to_string(read_out):
        """
        get a float-list and return it as a string separated by piping
        :param read_out: list with floats
        :return: floats rounded on 2 concatenated with piping
        """
        read_out_string = ''
        for i in range(len(read_out)):
            if read_out_string != '':
                read_out_string = read_out_string + ' | '
            read_out_string = read_out_string + str(round(read_out[i], 2))
        return read_out_string

    def get_last_read_out_string(self):
        return self.convert_float_list_to_string(self.read_outs[-1])

    def get_sensor_values(self, sensor):
        values = []
        for i in range(len(self.read_outs)):
            read_out = self.read_outs[i]
            values.append(round(read_out[sensor], 2))
        return values

    def get_time_string(self):
        now = self.datetime.datetime.now()
        return now.strftime("%H:%M")

    def get_sensor_data(self):
        """
        Get a timestamp and a readout from all sensors. Return them as an array
        """
        sensor = [self.read_sensor(channel=0), self.read_sensor(channel=1), self.read_sensor(channel=2)]
        return sensor

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
        Also keep last 10 readouts in variable
        """
        read_out = self.get_sensor_data()
        self.log.info('Moisture read-out: ' + self.convert_float_list_to_string(read_out))
        self.add_read_outs(read_out)


if __name__ == '__main__':
    # run this class stand alone o test class
    import sys
    import time
    from Logger import Logger

    logger = Logger(log_level=10, log_name='test sensor')
    mcp3008 = MCP3008(log_name='test sensor')
    while True:
        try:
            mcp3008.set_read_outs()
            print(mcp3008.get_last_read_out_string())
            time.sleep(1)
        except KeyboardInterrupt as e:
            print("Quit the Loop")
            sys.exit()
