#!/usr/bin/env python
from flask import Flask, render_template, session, request
import sys
import subprocess
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bankapp450i46##'

# Route for serving up the index page
@app.route('/')
def index():
    return render_template(
        'client/index.html',
         nodeaddress = nodeaddress
    )



