from MoistureSensor import MoistureSensor
from main import MainClass
from flask import Flask, render_template, request
from flask import render_template, redirect, url_for, Markup

app = Flask(__name__)
app.config["DEBUG"] = True
mainClass = MainClass()
disable_automatic_sprinkling = "Disable automatic sprinkling"
enable_automatic_sprinkling = "Enable automatic sprinkling"


@app.route('/')
def index():
    return 'Hello world'


@app.route("/home", methods=['GET', 'POST'])
def home():
    # Line chart data (moisture)
    moisture_labels = mainClass.moistureSensors.get_sensor_data_times()
    moisture_values0 = mainClass.moistureSensors.get_sensor_data(0)
    moisture_values1 = mainClass.moistureSensors.get_sensor_data(1)
    moisture_values2 = mainClass.moistureSensors.get_sensor_data(2)

    # Bar chart data (Temperature)
    temperature = mainClass.humiditySensor.get_temperature()
    humidity = mainClass.humiditySensor.get_humidity()
    colour0 = 'rgba(122, 193, 239, 0.3)'
    colour1 = 'rgba(122, 193, 239, 1)'
    if temperature >= 0:
        colour0 = 'rgba(206, 21, 52, 0.3)'
        colour1 = 'rgba(206, 21, 52, 1)'
    temperature_colour0 = [colour0, 'rgba(9, 170, 10, 0.3)']
    temperature_colour1 = [colour1, 'rgba(9, 170, 10, 1)']

    temperature_values = [temperature, humidity]

    # auto sprinkling setting
    auto_onoff = enable_automatic_sprinkling
    if mainClass.auto_sprinkling:
        auto_onoff = disable_automatic_sprinkling

    if request.method == 'POST':
        if request.form.get('action1') == 'Activate Pump 1':
            mainClass.activate_pump(0)
        elif request.form.get('action2') == 'Activate Pump 2':
            mainClass.activate_pump(1)
        elif request.form.get('action3') == 'Activate Pump 3':
            mainClass.activate_pump(2)
        elif request.form.get('action4') == disable_automatic_sprinkling:
            mainClass.auto_sprinkling = False
            auto_onoff = enable_automatic_sprinkling
        elif request.form.get('action4') == enable_automatic_sprinkling:
            mainClass.auto_sprinkling = True
            auto_onoff = disable_automatic_sprinkling
        else:
            pass  # unknown
    elif request.method == 'GET':
        return render_template('home.html', max=100, moisture_labels=moisture_labels,
                               moisture_values0=moisture_values0, moisture_values1=moisture_values1,
                               moisture_values2=moisture_values2, temperature_values=temperature_values,
                               temperature_colour0=temperature_colour0, temperature_colour1=temperature_colour1,
                               auto_onoff=auto_onoff)

    return render_template('home.html', max=100, moisture_labels=moisture_labels,
                           moisture_values0=moisture_values0, moisture_values1=moisture_values1,
                           moisture_values2=moisture_values2, temperature_values=temperature_values,
                           temperature_colour0=temperature_colour0, temperature_colour1=temperature_colour1,
                           auto_onoff=auto_onoff)


try:
    mainClass.start_sensor_thread()
    mainClass.power_led_program_running()
    app.run(debug=False, port=mainClass.web_port_number, host='0.0.0.0')
    print('Killing program....')
    mainClass.log.debug('Web interface keyboard interruption')
    mainClass.end_sensor_thread()
    mainClass.moistureSensors.close()
    mainClass.deactivate_power_led()
    mainClass.cleanup_gpio()
except Exception as Argument:
    mainClass.powerLed.led_set("RED")
    mainClass.log.exception("Error occurred web running")


