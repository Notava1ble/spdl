import argparse
import os
import logging
import sys
from app import App
from parser import Args, parse_args
from utils import get_token, trackname_convention
from logging_config import setup_logging


def main():
    args: Args = parse_args()
    outpath: str = os.path.join(os.getcwd(), args.outpath)
    logging.debug(f"Output path: {outpath}")
    app: App = App(outpath=outpath)

    if args.sync:
        # handle_sync_file(os.path.abspath(args.sync))
        ...
    else:
        token = get_token()
        _, set_trackname_convention = trackname_convention()

        app.set_links(args.link)
        app.outpath = args.outpath

    print("\n" + "-" * 25 + " Task complete ;) " + "-" * 25 + "\n")


if __name__ == "__main__":
    try:
        setup_logging()
        logging.info("-" * 10 + "Program started" + "-" * 10)
        main()
        logging.info("-" * 10 + "Program ended" + "-" * 10)
    except KeyboardInterrupt:
        print("\n------ Exiting program ------")
        logging.info("Program exited by user")
