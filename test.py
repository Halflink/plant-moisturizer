class Test:
    from JsonHandler import JsonHandler
    import RPi.GPIO as GPIO
    import time as time

    class PowerLed:

        def __init__(self, GPIO, led_gpio):
            self.GPIO = GPIO
            self.red_gpio = led_gpio[0]
            self.green_gpio = led_gpio[1]
            self.blue_gpio = led_gpio[2]
            self.GPIO.setmode(GPIO.BCM)
            self.GPIO.setup(self.red_gpio, self.GPIO.OUT)
            self.GPIO.setup(self.green_gpio, self.GPIO.OUT)
            self.GPIO.setup(self.blue_gpio, self.GPIO.OUT)

        def led_off(self):
            rgb = [False, False, False]
            self.led_set(rgb)

        def led_set(self, rgb):
            if rgb is not None:
                if rgb[0]:
                    self.GPIO.output(self.red_gpio, self.GPIO.HIGH)
                else:
                    self.GPIO.output(self.red_gpio, self.GPIO.LOW)

                if rgb[1]:
                    self.GPIO.output(self.green_gpio, self.GPIO.HIGH)
                else:
                    self.GPIO.output(self.green_gpio, self.GPIO.LOW)

                if rgb[2]:
                    self.GPIO.output(self.blue_gpio, self.GPIO.HIGH)
                else:
                    self.GPIO.output(self.blue_gpio, self.GPIO.LOW)

        def led_on(self, colour):
            rgb = None
            if colour == 'RED':
                rgb = [True, False, False]
            elif colour == 'GREEN':
                rgb = [False, True, False]
            elif colour == 'BLUE':
                rgb = [False, False, True]
            elif colour == 'CYAN':
                rgb = [False, True, True]
            elif colour == 'MAGNENTA':
                rgb = [True, False, True]
            elif colour == 'Yellow':
                rgb = [True, True, False]
            else:
                rgb = [True, True, True]
            self.led_set(rgb)

    def __init__(self):
        json_handler = self.JsonHandler()

        self.rgb_led_gpio = json_handler.rgb_led_gpio
        self.led = self.PowerLed(self.GPIO, self.rgb_led_gpio)

    def testTest(self):
        self.led.led_on('RED')
        self.time.sleep(2)
        self.led.led_on('YELLOW')
        self.time.sleep(2)
        self.led.led_on('GREEN')
        self.time.sleep(2)
        self.led.led_on('CYAN')
        self.time.sleep(2)
        self.led.led_on('BLUE')
        self.time.sleep(2)
        self.led.led_on('MAGNENTA')
        self.time.sleep(2)
        self.led.led_on('doemaarwa')


if __name__ == '__main__':
    # If main is started, it will test the RGB led
    test = Test()
    test.testTest()
