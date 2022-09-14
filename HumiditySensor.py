class HumiditySensor:
    """
        Class for DHT22 sensor
    """
    # import
    import Adafruit_DHT

    def __init__(self):
        self.DHT_SENSOR = self.Adafruit_DHT.DHT22
        self.DHT_PIN = 4


if __name__ == '__main__':
    # run this class stand alone o test class
    humiditySensor = HumiditySensor()

    while True:
        humidity, temperature = humiditySensor.Adafruit_DHT.read_retry(humiditySensor.DHT_SENSOR,
                                                                       humiditySensor.DHT_PIN)

        if humidity is not None and temperature is not None:
            print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
        else:
            print("Failed to retrieve data from humidity sensor")
