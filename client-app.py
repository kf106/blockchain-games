#!/usr/bin/env python
from flask import Flask, render_template, session, request
import sys
import subprocess
import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from time import sleep

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clientapp450i46##'

###
# Blockchain functions
###

multichainCli = "multichain-cli -datadir=~/.multichain-player -port=19255 -rpcport=19254 game " 

def getAddress():
  obj = json.loads(subprocess.check_output([multichainCli + "listpermissions connect"], shell=True))
  address = obj[0]['address']
  return address

playerAddress = getAddress()
# always publish own address on root stream when you start playing
# write to result: we may need it at some point
result = ([multichainCli + "publish root playerEntry '{\"json\":{\"address\":\"" + playerAddress + "\"}}'"], shell=True)

def getName():
  # use getstreampublishersummary to ensure only player's updates are examined
  obj_s = (subprocess.check_output([multichainCli + "getstreampublishersummary root " + playerAddress + " jsonobjectmerge"], shell=True))
  obj = json.loads(obj_s)
  print("SUMMARY")
  print(obj)
  if 'name' in obj['json']:
      name = obj['json']['name']
  else:
      name =  "Name not set"
  return name

def writeName(newName):
  writeString = multichainCli + "publish root playerEntry '{\"json\":{\"name\":\"" + newName + "\"}}'"
  obj_s = subprocess.check_output([multichainCli + "publish root playerEntry '{\"json\":{\"name\":\"" + newName + "\"}}'"], shell=True)
  return

def getNodeAddress():
  obj = json.loads(subprocess.check_output([multichainCli + "getinfo"], shell=True))
  nodeaddress = obj['nodeaddress']
  return nodeaddress

def getBalances():
  balances_array = json.loads(subprocess.check_output([multichainCli + "gettotalbalances"], shell=True))
  balances = {}
  for item in balances_array:
      print(item)
      balances.update( {item['name']: item['qty']} )
  return balances

###
#  WTForms
###

class NameForm(FlaskForm):
    playername = StringField('Playername', validators=[DataRequired()])
    submit = SubmitField('Update')

###
# Routes for player pages
###

# Route for serving up the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
   
    if request.method == 'POST':
        if form.validate() == False:
            # validate here
            print("NameForm didn't validate")
        else:
            print("Got the NameForm with " + form.playername.data )
            writeName(form.playername.data)
            sleep(5)
    balances = getBalances()
    return render_template(
        'client/index.html',
        currentname = getName(),
        address = playerAddress,
        gold = balances["gold"],
        xp = balances["xp"],
        form = NameForm()
    )    



