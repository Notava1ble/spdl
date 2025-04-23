import argparse
import os
import logging
import sys
from utils import get_token, trackname_convention
from downloader import check_track_playlist
from sync import handle_sync_file
from logging_config import configure_logger


def main():
    args = parse_args()

    if args.sync:
        sync_path = os.path.abspath(args.sync)
        logging.debug("sync path arg: %s", sync_path)
        handle_sync_file(sync_path)
    else:
        logging.debug("Getting token")
        token = get_token()
        _, set_trackname_convention = trackname_convention()
        logging.debug(
            "Set trackname convention to: %s, %s", set_trackname_convention, _
        )
        for link in args.link:
            logging.debug("Working with link: %s", link)
            check_track_playlist(
                link,
                args.outpath,
                create_folder=args.folder,
                trackname_convention=set_trackname_convention,
                token=token,
            )

    logging.info("\n" + "-" * 25 + " Task complete ;) " + "-" * 25 + "\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Program to download tracks from Spotify via CLI"
    )
    parser.add_argument("-link", nargs="+", help="URL of the Spotify track or playlist")
    parser.add_argument(
        "-outpath",
        nargs="?",
        default=os.getcwd(),
        help="Path to save the downloaded track",
    )
    parser.add_argument(
        "-sync",
        nargs="?",
        const="sync.json",
        help="Path of sync.json file to sync local playlist folders with Spotify playlists",
    )
    parser.add_argument(
        "-folder", nargs="?", default=True, help="Create a folder for the playlist(s)"
    )

    return parser.parse_args()


if __name__ == "__main__":
    try:
        configure_logger()
        logging.debug("-" * 10 + "Program started" + "-" * 10)
        main()
        logging.debug("-" * 10 + "Program ended" + "-" * 10)
    except KeyboardInterrupt:
        logging.debug("Program exited by user")
