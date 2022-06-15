from flask import Flask
from flask import render_template, redirect, url_for, Markup
app = Flask(__name__)
app.config["DEBUG"] = True

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.route('/')
def index():
    return 'Hello world'


@app.route("/home")
def home():
    line_labels = labels
    line_values = values
    return render_template('home.html', title='Bitcoin Monthly Price in USD', max=17000, labels=line_labels,
                           values=line_values)


if __name__ == '__main__':

    app.run(debug=True, port=5001, host='0.0.0.0')
