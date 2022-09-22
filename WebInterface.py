from MoistureSensor import MoistureSensor
from main import MainClass
from flask import Flask, render_template, request
from flask import render_template, redirect, url_for, Markup

app = Flask(__name__)
app.config["DEBUG"] = True
mainClass = MainClass()


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

    if request.method == 'POST':
        if request.form.get('action1') == 'Activate Pump 1':
            mainClass.activate_pump(0)
        elif request.form.get('action2') == 'Activate Pump 2':
            mainClass.activate_pump(1)
        elif request.form.get('action3') == 'Activate Pump 3':
            mainClass.activate_pump(2)
        else:
            pass  # unknown
    elif request.method == 'GET':
        return render_template('home.html', max=100, moisture_labels=moisture_labels,
                               moisture_values0=moisture_values0, moisture_values1=moisture_values1,
                               moisture_values2=moisture_values2, temperature_values=temperature_values,
                               temperature_colour0=temperature_colour0, temperature_colour1=temperature_colour1)

    return render_template('home.html', max=100, moisture_labels=moisture_labels,
                           moisture_values0=moisture_values0, moisture_values1=moisture_values1,
                           moisture_values2=moisture_values2, temperature_values=temperature_values,
                           temperature_colour0=temperature_colour0, temperature_colour1=temperature_colour1)


# if __name__ == '__main__':
try:
    mainClass.start_sensor_thread()
    mainClass.activate_power_led()
    mainClass.time.sleep(2)
    app.run(debug=True, port=mainClass.web_port_number, host='0.0.0.0')
    print('Killing program....')
    mainClass.log.debug('Web interface keyboard interruption')
    mainClass.moistureSensors.close()
    mainClass.deactivate_power_led()
    mainClass.cleanup_gpio()
except KeyboardInterrupt as e:
    print('Killing program....')
    mainClass.log.debug('Web interface keyboard interruption')
    mainClass.moistureSensors.close()
    mainClass.deactivate_power_led()
    mainClass.cleanup_gpio()


