#!/usr/bin/env python
from flask import Flask, render_template, session, request
import sys
import subprocess
import json


obj = json.loads(subprocess.check_output(["multichain-cli game listpermissions issue"], shell=True))
bankaddress = obj[0]['address']
print("Main address")
print(bankaddress)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bankapp450i46##'

# Route for serving up the index page
@app.route('/')
def index():
    balances_json = json.loads(subprocess.check_output(["multichain-cli game gettotalbalances"], shell=True))
    players_json = json.loads(subprocess.check_output(["multichain-cli game listaddresses"], shell=True))
    return render_template(
        'bank/index.html',
         balances = json.dumps(balances_json, sort_keys = True, indent = 4, separators = (',', ': ')),
         players = json.dumps(players_json, sort_keys = True, indent = 4, separators = (',', ': '))
    )


@app.route('/bank/signup', methods=['POST'])
def login():
    if request.method == 'POST':
        return render_template('bank/signup_success.html')       
    else:
       return render_template('bank/signup_error.html') 

