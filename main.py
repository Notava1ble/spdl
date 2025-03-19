import argparse
import os
import logging
import sys
from app import App
from parser import parse_args
from utils import get_token, trackname_convention
from downloader import check_track_playlist
from sync import handle_sync_file
from logging_config import setup_logging


def main():
    app = App()
    args = parse_args()

    if args.sync:
        handle_sync_file(os.path.abspath(args.sync))
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
