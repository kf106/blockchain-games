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
    multichaind -datadir=~/.multichain-player -port=19255 -rpcport=19254 -reindex=1 game -daemon
  fi
else
  if [ -z "$1" ]
  then
    echo -e "No blockchain address supplied"
	exit 0
  else
    # create multichain player instance by connecting to asset bank, extract your local address
    # and send it to the asset bank webserver for automatic connection
    mkdir ~/.multichain-player
    gameblockchain=$1
    myaddress=$(multichaind -datadir=~/.multichain-player -port=19255 -rpcport=19254 $1 | grep -P -i -o '(?<=grant )\S+' | sed -r 's/^\W|\W$//g')
    echo -e "My address: $myaddress"
    # now we get the asset bank's IP address from the command line $1 parameter
    assetbankip=${gameblockchain%:*}  # retain the part before :
    assetbankip=${assetbankip##*@}  # retain the part after @
    echo -e "Server IP: $assetbankip"
    # POST 
echo $NAME
  fi
fi

# this runs the application
# echo -e "Starting client interface"
# export FLASK_RUN_PORT=5001
# flask run --host=0.0.0.0
