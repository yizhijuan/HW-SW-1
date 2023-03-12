from flask import Flask, render_template, session
from flask_session import Session
import serial, bluetooth

app = Flask(__name__)
data_list = []
filename = 'Wave_data.txt'
port = '/dev/cu.usbserial-0001'
baudrate = 9600

app.secret_key = 'mysecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


def read_serial_data(port, baudrate, data_list, filename):
    ser = serial.Serial(port, baudrate)
    while True:
        data = ser.readline().decode()
        write_to_file(filename, data)
        data_list.append(data)

def write_to_file(filename, data):
    with open(filename, 'a') as f:
        #f.write(data + '\n')
        f.write(data)
    
@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/start')
def start():
    global data_list
    data_list = []
    read_serial_data(port, baudrate, data_list, filename)
    return 'Reading started'

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

# keep reading, store them to a list or a file.
# when I click the button, pass the latest word and render the page.

@app.route("/recog", methods=['POST'])
def recog():
    latest = data_list[-1] if data_list else ''
    latest_msg = latest.rstrip()      # decode byte string into Unicode
    print(f"latest_msg: {latest_msg}")  
    word = number_to_word.get(latest_msg, 'invalid')
    # Add the word to a list in the session data
    if 'words' not in session:
        session['words'] = []
    session['words'].append(word)
    return render_template('bluetooth.html', data = session['words'])


if __name__ == "__main__":
    app.run(debug=True)
