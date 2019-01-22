#!/usr/bin/env python
from flask import Flask, render_template, session, request
import sys
import subprocess
import json
from flask_socketio import SocketIO, emit, disconnect
from random import random
from threading import Lock

###
# Load values from blockchain
###

def getBankAddress():
  obj = json.loads(subprocess.check_output(["multichain-cli game listpermissions issue"], shell=True))
  bankaddress = obj[0]['address']
  return bankaddress

def getNodeAddress():
  obj = json.loads(subprocess.check_output(["multichain-cli game getinfo"], shell=True))
  nodeaddress = obj['nodeaddress']
  return nodeaddress

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
# Personally, I install and use eventlet
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bankapp450i46##'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

# The websocket is maintained in the background, and this
# function outputs a random number every 5 seconds
def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(5)
        count += 1
        number = round(random()*10, 3)
        socketio.emit('my_response',
                      {'data': number, 'count': count},
                      namespace='/live')
###
# Websocket pages
###

# Route for serving up the index page
@app.route('/live')
def live():
    return render_template('/bank/live.html', async_mode=socketio.async_mode)

# This function is called when a web browser connects
@socketio.on('connect', namespace='/live')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})

# Ping-pong allows Javascript in the web page to calculate the
# connection latency, averaging over time
@socketio.on('my_ping', namespace='/live')
def ping_pong():
    emit('my_pong')

# Notification that a client has disconnected
@socketio.on('disconnect', namespace='/live')
def test_disconnect():
    print('Client disconnected', request.sid)

###
# Static pages
###

# Route for serving up the index page
@app.route('/')
def index():
    return render_template(
        'bank/index.html',
         nodeaddress = getNodeAddress()
    )

# Route for serving up the admin page
@app.route('/admin')
def admin():
    balances_json = json.loads(subprocess.check_output(["multichain-cli game gettotalbalances"], shell=True))
    players_json = json.loads(subprocess.check_output(["multichain-cli game listaddresses"], shell=True))
    return render_template(
        'bank/admin.html',
         balances = json.dumps(balances_json, sort_keys = True, indent = 4, separators = (',', ': ')),
         players = json.dumps(players_json, sort_keys = True, indent = 4, separators = (',', ': '))
    )

# Route for automatic player signup
@app.route('/signup', methods=['POST'])
def login():
    if request.method == 'POST':
        # get posted address (should do error checking on this)
        sent_address = request.get_json()['address']
        print("I got the following address:")
        print(sent_address)
        # grant connect send and receive
        result = subprocess.check_output(["multichain-cli game grant " + sent_address + " connect,send,receive"], shell=True)
        print(result)
        # asset bank imports all addresses
        result = subprocess.check_output(["multichain-cli game importaddress " + sent_address + " true"], shell=True)
        print(result)           
        # issue more of the assets (gold and xp) to the new address
        result = subprocess.check_output(["multichain-cli game issuemore " + sent_address + " gold 100"], shell=True)
        print(result)    
        result = subprocess.check_output(["multichain-cli game issuemore " + sent_address + " xp 1"], shell=True)
        print(result)    
        return render_template('bank/signup_success.html')       
    else:
        return render_template('bank/signup_error.html') 

# Run the web app
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')

