import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading


def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()


class NetCat:

    # Initialize the NetCat object
    def __init__(self, args, buffer=None):
        self.args = True
        self.buffer = buffer
        # Create the socket object
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def send(self):
        pass

    def listen(self):
        pass

    def run(self):
        # If we're setting up a listener, call the listen method
        if self.args.listen:
            self.listen()
        else:
        # otherwise call the send method
            self.send()


def main():
    # Using argparse module to create a CLI
    parser = argparse.ArguemntParser(
        description="BHP Net Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # Example of usage to the user when they type --help
        epilog=textwrap.dedent(
            """
            Example:
            netcate.py -t 102.168.1.108 -p 5555 -l -c # command shell
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
            echo 'ABCDEFGHI' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
            netcat.py -t 192.168.1.108 -p 5555 # connect to server
            """
        ),
    )
    # The six arguments that specify the behavior of the program

    # -c sets up an interactive shell
    parser.add_argument("-c", "--command", action="store_true", help="command shell")
    # -e executes one specific command
    parser.add_argument("-e", "--execute", help="Execute specified command")
    # -l indicates that a listener should be set up
    parser.add_argument("-l", "--listen", action="store_true", help="Listen")
    # -p specifies the por on hich to communicate
    parser.add_argument("-p", "--port", type=int, default=5555, help="Specified port")
    # -t specifies the target IP
    parser.add_argument("-t", "--target", default="192.168.1.203", help="Specified IP")
    # -u specifies the name of a file to upload
    parser.add_argument("-u", "--upload", help="Upload file")

    args = parser.parse_args()
    if args.listen:
        # If we are settring up a listener, we need to buffer the input
        buffer = ""
    else:
        # Otherwise, we send the buffer content from stdin
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    nc.run()


if __name__ == "__main__":
    main()
