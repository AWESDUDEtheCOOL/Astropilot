from flask import Flask, render_template, request
from alert import *

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

if __name__ == '__main__':
    app.run(debug=True)