#!/bin/bash
# (C) 2019 Keir Finlow-Bates
# See LICENSE for the licensing details of this software

if [ -z $BASH_VERSION ] ; then
	echo "You must run this script using bash" 1>&2
	exit 1
fi

set -x

# This script uses python3.
# Activate the virtual python3 environment
source venv/bin/activate

# Proof of concept - so minimal error checking!

# check if game blockchain has already been connected to
# if it is not running, start it
# if it does not exist, create it

# the asset bank is run in the default directory .multichain.
# game nodes are run in a .multichain-player
# two blockchains to work on one machine


if [ -e ~/.multichain-player/game/params.dat ]
then
  echo -e "Game blockchain already exists."
  multichain-cli -datadir=~/.multichain-player -port=19255 -rpcport=19254 game getinfo
  if [ $? -eq 0 ]
  then
    echo -e "Game player blockchain is running."
  else
    echo -e "Starting game player blockchain daemon."
    # run with reindex in case there was a broken shutdown
    multichaind -datadir=~/.multichain-player -port=19255 -rpcport=19254 game -reindex=1 -daemon
  fi
else
  # create multichain player instance by connecting to asset bank, extract your local address
  # and send it to the asset bank webserver for automatic connection
  mkdir ~/.multichain-player
  multichaind -datadir=.multichain-player -port=19255 -rpcport=19254 $1 
  myaddress=$(multichaind -datadir=~/.multichain-player -port=19255 -rpcport=19254 $1)
  #  | python -c "import json,sys;obj=json.load(sys.stdin);print(obj[0]['address']);"
  echo -e "My address: $myaddress"
fi

# this runs the application
#echo -e "Starting asset bank interface"
#export FLASK_APP=bank-app.py
#flask run --host=0.0.0.0
