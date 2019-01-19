#!/bin/bash
# (C) 2019 Keir Finlow-Bates

if [ -z $BASH_VERSION ] ; then
	echo -e "You must run this script using bash." 1>&2
	exit 1
fi

# Make sure we are running as root
if [[ $EUID -ne 0 ]]; then
	echo -e "This script must be run as root." 1>&2
	exit 1
fi

echo -e ""
echo -e "--------------------------------------------------------------------------------"
echo -e "Installing MultiChain                                            "
echo -e "--------------------------------------------------------------------------------"
echo -e ""

MCFILE="multichain-2.0-beta-1"
echo  -e "Current multichain is ${MCFILE}"

# Check whether we need to install MultiChain
if test -x /usr/local/bin/multichaind ; then
	echo -e "MultiChain already installed"
else
	cd /tmp
	wget "https://www.multichain.com/download/${MCFILE}.tar.gz"
	tar -xvzf "${MCFILE}.tar.gz"
	cd "${MCFILE}"
	mv multichaind multichain-cli multichain-util /usr/local/bin
fi
