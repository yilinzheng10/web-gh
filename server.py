import os
import time
import json
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', image_path="", form_data={})


@app.route('/', methods=['POST'])
def submit():

    form_data = request.form.to_dict()

    with open('static/inputs.txt', 'w') as f:
        json.dump(form_data, f)

    if os.path.exists('static/screenshot.jpg'):
        os.remove('static/screenshot.jpg')

    while not os.path.exists('static/screenshot.jpg'):
        time.sleep(1)

    return render_template('index.html', image_path="static/screenshot.jpg", form_data=form_data)
