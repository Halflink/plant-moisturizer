from MCP3008 import MCP3008
from main import MainClass
from flask import Flask, render_template, request
from flask import render_template, redirect, url_for, Markup

app = Flask(__name__)
app.config["DEBUG"] = True
mainClass = MainClass()

labels = []
values = []


def add_label(current_time):
    labels.append(current_time)
    if len(labels) > 11:
        labels.pop(0)


def add_value(value):
    rounded_value = 10 * round(value, 3)
    values.append(rounded_value)
    if len(values) > 11:
        values.pop(0)


colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.route('/')
def index():
    return 'Hello world'


@app.route("/home", methods=['GET', 'POST'])
def home():
    sensor_timestamp = mainClass.sensors.get_sensor_timestamp()
    add_label(sensor_timestamp[0])
    add_value(sensor_timestamp[1])
    line_labels = labels
    line_values = values

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
        return render_template('home.html', title='Moisture sensor', max=30, labels=line_labels,
                               values=line_values)

    return render_template('home.html', title='Moisture sensor', max=30, labels=line_labels,
                           values=line_values)


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
