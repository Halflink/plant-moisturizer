from MCP3008 import MCP3008
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
    line_labels = mainClass.sensors.time_read_outs
    line_values = mainClass.sensors.get_sensor_values(0)

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
    mainClass.start_sensor_thread()
    app.run(debug=True, port=5001, host='0.0.0.0')
