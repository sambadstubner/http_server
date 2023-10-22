import argparse
import logging
import os
import sys


class ServerHelpFormatter(argparse.HelpFormatter):
    def __init__(
        self,
        prog: str,
        indent_increment: int = 2,
        max_help_position: int = 24,
        width: int | None = None,
    ) -> None:
        super().__init__(prog, indent_increment, max_help_position, width)


class ServerParser(argparse.ArgumentParser):
    help = """usage: http_server.py [-h] [-p PORT] [-v] [-d] [-f FOLDER]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port to bind to
  -v, --verbose         turn on debugging output
  -d, --delay           add a delay for debugging purposes
  -f FOLDER, --folder FOLDER
                        folder from where to serve from"""

    DEFAULT_PORT = 8084

    def __init__(self):
        super().__init__(
            formatter_class=ServerHelpFormatter, usage=argparse.SUPPRESS, add_help=False
        )
        self.add_argument("-h", "--help", action="store_true")
        self.add_argument(
            "-p",
            "--port",
            default=self.DEFAULT_PORT,
            type=int,
            help="port to bind to",
            required=False,
        )
        self.add_argument(
            "-v",
            "-verbose",
            action="store_true",
            help="turn on debugging output",
            required=False,
        )
        self.add_argument(
            "-d",
            "--delay",
            action="store_true",
            help="add a delay for debugging purposes",
        )
        self.add_argument(
            "-f",
            "--folder",
            default=".",
            help="folder from where to serve from",
            type=self.dir_path,
        )

        self.parse()

    @staticmethod
    def dir_path(string):
        if os.path.isdir(string):
            return string
        else:
            raise NotADirectoryError(string)

    def parse(self):
        try:
            self.args = self.parse_args()

        except:
            print(self.help)
            sys.exit(0)

        self.handle_help()
        self.handle_verbose()

    def handle_help(self):
        if self.args.help:
            print(self.help)
            sys.exit(0)

    def handle_verbose(self):
        if self.args.v:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.ERROR)


if __name__ == "__main__":
    parser = ServerParser()
