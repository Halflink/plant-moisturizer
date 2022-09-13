class MCP3008:
    """
        Class for MCP3008 ADC
        Using the MCP3008 chip to rad out the sensors.

        sensor_data_matrix:
            x: sensor_no (sensor 0, sensor 1, sensor 2)
            y: reading_no (reading 0, reading 1,.... reading 9)
    """
    from spidev import SpiDev
    import logging
    import datetime

    # Variables
    sensor_data_matrix = []
    sensor_data_times = []

    def __init__(self, log_name='', bus=0, device=0, readout_history_length=10):
        self.bus, self.device, self.readout_history_length = bus, device, readout_history_length
        self.spi = self.SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000  # 1MHz
        self.log = self.logging.getLogger(log_name)

    def add_sensor_data(self, sensor_data):
        # record read out and time of read out
        self.sensor_data_matrix.append(sensor_data)
        if len(self.sensor_data_matrix) > self.readout_history_length:
            self.sensor_data_matrix.pop(0)  # keep only 10 readouts in the array
        self.sensor_data_times.append(self.get_time_string)
        if len(self.sensor_data_times) > self.readout_history_length:
            self.sensor_data_times.pop(0) # keep only 10 readouts in the array

    def close(self):
        self.spi.close()

    @staticmethod
    def convert_list_to_string(read_out):
        """
        get a float-list and return it as a string separated by piping
        :param read_out: list with floats
        :return: floats rounded on 2 concatenated with piping
        """
        read_out_string = ''
        for i in range(len(read_out)):
            if read_out_string != '':
                read_out_string = read_out_string + ' | '
            read_out_string = read_out_string + str(read_out[i])
        return read_out_string

    def get_last_read_out_string(self):
        return self.convert_list_to_string(self.sensor_data_matrix[-1])

    def get_sensor_data(self, sensor_no):
        values = []
        for i in range(len(self.sensor_data_matrix)):
            sensor_data = self.sensor_data_matrix[i]
            values.append(round(sensor_data[sensor_no], 2))
        return values

    def get_sensor_data_times(self):
        values = []
        for i in range(len(self.sensor_data_times)):
            time_stamp = self.sensor_data_times[i]
            values.append(time_stamp)
        return values

    @staticmethod
    def get_time_string(self):
        now = self.datetime.datetime.now()
        return now.strftime("%H:%M")

    def open(self):
        # connect spi object to spi device
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000  # 1MHz

    def read_sensor(self, channel=0):
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

        # max value is 100. So divide by 10 and round
        value = round(data/10, 0)
        return value

    def write_sensor_read_out(self):
        """
        Read out all sensors and write them to file
        Also keep last 10 readouts in variable
        """
        read_out = [self.read_sensor(channel=0), self.read_sensor(channel=1), self.read_sensor(channel=2)]
        self.log.info('Moisture read-out: ' + self.convert_list_to_string(read_out))
        self.add_sensor_data(read_out)


if __name__ == '__main__':
    # run this class stand alone o test class
    import sys
    import time
    from Logger import Logger

    logger = Logger(log_level=10, log_name='test sensor')
    mcp3008 = MCP3008(log_name='test sensor')
    while True:
        try:
            mcp3008.write_sensor_read_out()
            print(mcp3008.get_last_read_out_string())
            time.sleep(1)
        except KeyboardInterrupt as e:
            print("Quit the Loop")
            sys.exit()
