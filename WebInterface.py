from MoistureSensor import MoistureSensor
from main import MainClass
from flask import Flask, render_template, request
from flask import render_template, redirect, url_for, Markup

app = Flask(__name__)
app.config["DEBUG"] = True
mainClass = MainClass()

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.route('/')
def index():
    return 'Hello world'


@app.route("/home", methods=['GET', 'POST'])
def home():
    # Line chart data (moisture)
    line_labels = mainClass.moistureSensors.get_sensor_data_times()
    line_values0 = mainClass.moistureSensors.get_sensor_data(0)
    line_values1 = mainClass.moistureSensors.get_sensor_data(1)
    line_values2 = mainClass.moistureSensors.get_sensor_data(2)

    # Doughnut chart data (Temperature)
    doughnut_labels = ['Temperature', '']
    doughnut_max = 50
    doughnut_temp = 30
    doughnut_untemp = doughnut_max - doughnut_temp
    pie_labels = ["A","B"]
    pie_values = [30,20]
    pie_colours = ["#F7464A", "#46BFBD"]

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
        return render_template('home.html', title='Moisture sensor', max=100, labels=line_labels,
                               values0=line_values0, values1=line_values1, values2=line_values2)

    return render_template('home.html', title='Moisture sensor', max=100, labels=line_labels,
                           values0=line_values0, values1=line_values1, values2=line_values2,
                           set=zip(pie_values, pie_labels, pie_colours))


if __name__ == '__main__':
    mainClass.start_sensor_thread()
    mainClass.time.sleep(2)
    app.run(debug=True, port=mainClass.web_port_number, host='0.0.0.0')
