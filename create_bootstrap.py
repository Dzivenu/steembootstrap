#!/usr/bin/env python3

import argparse
import base64
import bz2
import gzip
import json
import sys

from steem_watch import block_iterator
from steem_watch import steem_api

import tornado

async def main(argv, io_loop=None):
    parser = argparse.ArgumentParser(description="Create bootstrap files for Steem")
    parser.add_argument("-s", "--server", dest="server", metavar="WEBSOCKET_URL", help="Specify API server")
    parser.add_argument("-b", "--bootstrap", dest="bootstrap_filename", metavar="FILENAME", help="Specify bootstrap file")
    parser.add_argument("-n", "--blocks", default=-1, type=int, dest="blocks", metavar="NUM", help="Number of blocks to include")
    parser.add_argument("-d", "--date", default="", dest="date", metavar="DATE", help="Cutoff date (default today)")

    args = parser.parse_args(argv[1:])

    stop_date = ""
    if (args.blocks == -1) and (args.date == ""):
        stop_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    else:
        stop_date = args.date

    node = steem_api.ApiNode(io_loop=io_loop, websocket_url=args.server)
    node.start()
    await node.wait_for_connection()

    db_api = node.get_api("database_api")
    raw_block_api = node.get_api("raw_block_api")
    dgpo = await db_api.get_dynamic_global_properties()
    head_block_num = dgpo["head_block_number"]

    try:
        if args.bootstrap_filename.endswith(".gz"):
            f = gzip.open(args.bootstrap_filename, "wb")
        elif args.bootstrap_filename.endswith(".bz2"):
            f = bz2.open(args.bootstrap_filename, "wb")
        else:
            f = open(args.bootstrap_filename, "wb")

        block_num = 1
        while True:
            block = await raw_block_api.get_raw_block(block_num=block_num)
            if (stop_date != "") and (block["timestamp"] >= stop_date):
                break
            f.write( base64.b64decode(block["raw_block"]) )
            if (block_num % 10000) == 0:
                sys.stderr.write(str(block_num)+"\n")
                sys.stderr.flush()
            block_num += 1
            if (args.blocks > 0) and (block_num >= args.blocks):
                break
    finally:
        f.close()

def sys_main():
    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.run_sync(lambda : main(sys.argv, io_loop=io_loop))

if __name__ == "__main__":
    sys_main()
