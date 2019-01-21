# MultiChain Game Engine
This repository provides a sample setup for a blockchain-backed game, using MultiChain (http://www.multichain.com) as the backend blockchain. See game-blockchain.pdf for details of the game concepts.

The game contains two main components: the asset bank and the player client.
## Installation
For either asset bank or client run:

     sudo ./install.sh
     
This sets up the relevant Python virtual environment and install the required packages.

To run the asset bank, execute:

    ./bank-run.sh
    
This starts a local webserver. See http://localhost:5000/admin for the admin panel. Signup information for players is at http://localhost:5000/

To run the player client, execute:

     ./client-run.sh

## Asset Bank
The asset bank creates the original blockchain, issues assets (gold and xp in this example), issues further gold and xp as the bank's supplies run low, and automates player signup. 

## Player Client
The player client sets up a blockchain node, makes a signup request to the asset bank, and then launches the game. 

Subsequently it just launches the game, as the blockchain node only needs configuration once.

