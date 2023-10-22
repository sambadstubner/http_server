import logging
import os
from pathlib import Path
import signal
import socket
import sys
import time

import responses
from server_parser import ServerParser


class Server:
    DEFAULT_BUFFER_SIZE = 1024
    DEFAULT_DELAY_TIME = 5.0

    def __init__(self, port: int, folder: str, delay: bool = False):
        self.root = folder
        self.port = port
        self.delay = delay
        signal.signal(signal.SIGINT, self.handle_exit)

    def run(self):
        self.server_socket = socket.create_server(
            address=("", self.port), family=socket.AF_INET, reuse_port=True
        )
        self.server_socket.listen()

        while True:
            conn, address = self.server_socket.accept()
            logging.info(f"Connection from: {address}")

            while True:
                header = conn.recv(self.DEFAULT_BUFFER_SIZE)
                if not header:
                    logging.info("Client disconnected...")
                    break

                if self.delay:
                    logging.debug(f"Delaying {self.DEFAULT_DELAY_TIME} seconds")
                    time.sleep(self.DEFAULT_DELAY_TIME)

                action, resource = self.parse_header(header.decode())
                logging.debug(f"Action: {action} Resource: {resource}")

                self.send_response(conn, action, resource)

                logging.debug("Sent")
                break

            conn.close()

    @staticmethod
    def parse_header(header: str) -> (str, str):
        logging.debug(f"Header: \n{header}")
        action = Server.get_action_from_header(header)
        resource = Server.get_resource_from_header(header)
        return action, resource

    @staticmethod
    def get_action_from_header(header):
        space_index = header.index(" ")
        return header[:space_index]

    @staticmethod
    def get_resource_from_header(header):
        before_resource = header.index(" ")
        after_resource = header.index(" ", before_resource + 1)
        return header[before_resource + 1 : after_resource]

    def send_response(self, connection: socket, action: int, resource: str) -> int:
        logging.debug(f"Full resource path: {self.root + resource}")
        resource = self.root + resource
        # Currently only supporting GET requests
        if action == "GET":
            if not Path(resource).exists():
                response = responses.get_file_not_found()
                logging.debug(f"Invalid path. Sending: \n{response}")
                connection.send(response.encode())
            else:
                Server.send_resource(connection, resource)
        else:
            response = responses.get_method_not_allowed()
            logging.debug(f"Invalid action. Sending: \n{response}")
            connection.send(response.encode())

    @staticmethod
    def send_resource(connection: socket, resource: str):
        file_size = os.path.getsize(resource)
        logging.debug(f"File size: {file_size}")
        header = Server.create_header(200, "OK", file_size)
        logging.debug(f"Response Header: \n{header}")
        connection.send(header.encode())
        with open(resource, "rb") as file:
            while True:
                chunk = file.read(Server.DEFAULT_BUFFER_SIZE)
                if not chunk:
                    break
                logging.debug(f"Sending chunk: \n{chunk}")
                connection.send(chunk)

    @staticmethod
    def create_header(status_code, status_message, content_length):
        return f"""HTTP/1.0 {status_code} {status_message}
Content-Length: {content_length}

"""

    def handle_exit(self, sig, frame):
        logging.info("Interrupt detected, shutting down server...")
        self.server_socket.close()
        sys.exit(0)


if __name__ == "__main__":
    parser = ServerParser()
    server = Server(parser.args.port, parser.args.folder, parser.args.delay)
    server.run()
