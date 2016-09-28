
Create bootstrap.dat file.

Usage
-----

WARNING:  These build instructions are untested, YMMV.  Please open a ticket if they don't work for you.

Requires Python 3.5.  Instructions for Ubuntu 16.04:

    sudo apt-get install python-virtualenv
    virtualenv ~/ve/steem_bootstrap -p $(which python3)
    ~/ve/steem_bootstrap/bin/pip install https://github.com/theoreticalbts/steemwatch

Run with raw_block plugin/API in your config.ini, for example:

    rpc-endpoint = 127.0.0.1:8090
    public-api = database_api login_api block_info_api raw_block_api
    enable-plugin = witness account_history block_info raw_block

To create bootstrap file:

    ./create_bootstrap.py -s ws://127.0.0.1:8090 -d 2016-03-31 -b bootstrap.dat.bz2

Note this will take a long time to create a full bootstrap file.
