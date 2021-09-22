import argparse
import sys

from virgil import __version__, commands
from virgil.config import Config


def cli() -> None:
    Config.initialize()

    parser = argparse.ArgumentParser(description="Python dependency management utility")
    parser.add_argument("-v", "--version", action="version", version=__version__)

    subparsers = parser.add_subparsers()

    # Config
    parser_config = subparsers.add_parser(name="config", help="Print configuration")
    parser_config.set_defaults(func=commands.config_command)

    # List
    parser_list = subparsers.add_parser(name="list", help="List all dependencies")
    parser_list.add_argument("-r", "--requirements", action="append", help="Requirement file(s)")
    parser_list.set_defaults(func=commands.list_command)

    if len(sys.argv) == 1:
        # Print help if no arguments are passed
        parser.print_help()
    else:
        # Otherwise run the command
        args = parser.parse_args()
        args.func(args) if hasattr(args, "func") else parser.print_help()
