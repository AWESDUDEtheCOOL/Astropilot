from flask import Flask, render_template, request
from alert import *
from random import randrange

app = Flask(__name__)

@app.route("/")
def origin():
    return render_template('index.html')  # Assuming you have an 'index.html' template in the 'templates' directory

@app.route('/alert', methods=['POST'])
def run_script():
    # Get text input from the form
    call_title = 'alert'
    call_body = request.form['call_body']
    call_num = request.form['call_num']

    # Call the alert function
    alert(call_title, call_body, f'+1{call_num}')
    return render_template('index.html')

@app.route('/error', methods=['POST'])
def error():
    with open('responses.csv', 'r') as file:
        data = file.read().splitlines()
        data = [line.split(',') for line in data][1:]
    line = data[randrange(len(data))]
    error_msg = line[1]
    error_sev = line[2]
    if error_sev == 'Call':
        alert('Error', error_msg, '+12674107834')
    return render_template('index.html', message=error_msg)

if __name__ == '__main__':
    app.run(debug=True)