from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
import serial, bluetooth

app = Flask(__name__)
app.secret_key = 'mysecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/")
def bluetooth_data():
    session['words'] = []
    return render_template('bluetooth.html')

number_to_word = {
    '01000': 'one',
    '01100': 'two',
    '11100': 'three',
    '01111': 'four',
    '11111': 'five',
    '01110': 'six',
    '01101': 'seven',
    '01011': 'eight',
    '00111': 'nine',
    '10000': 'ten',
    '10001': 'number'   
}

@app.route("/recog", methods=['POST'])
def recog():
    #serialPort = '/dev/cu.ESP32-Old'
    serialPort = '/dev/cu.usbserial-0001'
    try:
        ser = serial.Serial(serialPort, 115200)
    except Exception as e:
        print(f"Error: {e}")
        return "Failed to connect to serial port."
    
    msg = ser.readline()         # read a byte string
    print(f"msg: {msg}")
    msg2 = msg.decode().rstrip()      # decode byte string into Unicode  
    word = number_to_word.get(msg2, 'invalid')
    # Add the word to a list in the session data
    if 'words' not in session:
        session['words'] = []
    session['words'].append(word)
    return render_template('bluetooth.html', data = session['words'])


if __name__ == "__main__":
    app.run(debug=True)
