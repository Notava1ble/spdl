import argparse
import os


def parse_args():
    # Initialize parser
    parser = argparse.ArgumentParser(
        description="Program to download tracks from Spotify via CLI"
    )

    group = parser.add_mutually_exclusive_group(required=True)

    # Add arguments
    group.add_argument(
        "-l",
        "--link",
        nargs="+",
        help="URL of the Spotify track or playlist",
    )
    parser.add_argument(
        "-p",
        "--outpath",
        nargs="?",
        default=os.getcwd(),
        help="Path to save the downloaded track",
    )
    group.add_argument(
        "-s",
        "--sync",
        nargs="?",
        const="sync.json",
        help="Path of sync.json file to sync local playlist folders with Spotify playlists",
    )
    parser.add_argument(
        "-f",
        "--folder",
        action="store_true",
        default=True,
        help="Create a folder for the playlist(s)",
    )

    return parser.parse_args()
