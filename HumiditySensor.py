class HumiditySensor:
    """
        Class for DHT22 sensor
    """
    # import
    import Adafruit_DHT
    import logging

    humidity = 0.0
    temperature = 0.0

    def __init__(self, log_name='', dht_pin=4):
        self.DHT_SENSOR = self.Adafruit_DHT.DHT22
        self.DHT_PIN = dht_pin
        self.log = self.logging.getLogger(log_name)

    def get_humidity_string(self):
        return "Humidity={0:0.1f}%".format(self.humidity)

    def get_temperature_string(self):
        return "Temp={0:0.1f}*C".format(self.temperature)

    def write_sensor_read_out(self):
        """
        Read out humidity sensor and write them to file
        Also keep last 10 readouts in variable
        """
        self.humidity, self.temperature = self.Adafruit_DHT.read_retry(humiditySensor.DHT_SENSOR,
                                                                       humiditySensor.DHT_PIN)
        if self.humidity is not None and self.temperature is not None:
            log_text = self.get_temperature_string() + ' ' + self.get_humidity_string()
        else:
            log_text = "Failed to retrieve data from humidity sensor"
        self.log.info('Moisture read-out: ' + log_text)


if __name__ == '__main__':
    # run this class stand alone o test class
    import time
    from Logger import Logger

    logger = Logger(log_level=10, log_name='test humidity sensor')
    humiditySensor = HumiditySensor(log_name='test sensor')

    while True:
        humiditySensor.write_sensor_read_out()

        if humiditySensor.humidity is not None and humiditySensor.temperature is not None:
            print(humiditySensor.get_temperature_string() + ' ' + humiditySensor.get_humidity_string())
        else:
            print("Failed to retrieve data from humidity sensor")

        time.sleep(3)
