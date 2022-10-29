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
                    self.GPIO.output(self.red_gpio, self.GPIO.LOW)
                else:
                    self.GPIO.output(self.red_gpio, self.GPIO.HIGH)

                if rgb[1]:
                    self.GPIO.output(self.green_gpio, self.GPIO.LOW)
                else:
                    self.GPIO.output(self.green_gpio, self.GPIO.HIGH)

                if rgb[2]:
                    self.GPIO.output(self.blue_gpio, self.GPIO.LOW)
                else:
                    self.GPIO.output(self.blue_gpio, self.GPIO.HIGH)

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
            elif colour == 'YELLOW':
                rgb = [True, True, False]
            else:
                rgb = [False, False, False]
            self.led_set(rgb)

    def __init__(self):
        json_handler = self.JsonHandler()

        self.rgb_led_gpio = json_handler.rgb_led_gpio
        self.led = self.PowerLed(self.GPIO, self.rgb_led_gpio)

    def testTest(self):
        self.led.led_on('RED')
        print("RED")
        self.time.sleep(5)
        self.led.led_on('YELLOW')
        print("YELLOW")
        self.time.sleep(5)
        self.led.led_on('GREEN')
        print("GREEN")
        self.time.sleep(5)
        self.led.led_on('CYAN')
        print("CYAN")
        self.time.sleep(5)
        self.led.led_on('BLUE')
        print("BLUE")
        self.time.sleep(5)
        self.led.led_on('MAGNENTA')
        print("MAGNENTA")
        self.time.sleep(5)
        self.led.led_off()



if __name__ == '__main__':
    # If main is started, it will test the RGB led
    test = Test()
    test.testTest()
