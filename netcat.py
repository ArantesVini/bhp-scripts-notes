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

    def handle(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())

        elif self.args.upload:
            file_buffer = b""
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data.decode()
                else:
                    break

            with open(self.args.upload, "wb") as f:
                f.write(file_buffer.encode())
            message = f"Save file {self.args.upload}"
            client_socket.send(message.encode())

        elif self.args.command:
            cmd_buffer = b""
            while True:
                try:
                    client_socket.send(b"BHP: #> ")
                    while "\n" not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b""
                except Exception as e:
                    print(f"Server killed {e}")
                    self.socket.close()
                    sys.exit()

    def send(self):
        # Connect to the target and port
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            # Start the loop to receive data from the target
            while True:
                recv_len = 1
                response = ""
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    # If there is no more data, break out of the loop
                    if recv_len < 4096:
                        break
                if response:
                    # Print the response, and wait for more input
                    print(response)
                    buffer = input(">")
                    buffer += "\n"
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            # The previous loop will run until the user presses Ctrl+C
            print("User terminated.")
            self.socket.close()
            sys.exit()

    def listen(self):
        # The listen method binds to the target and port
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            # Pass the connected socket to the handle method
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()

    def run(self):
        # If we're setting up a listener, call the listen method
        if self.args.listen:
            self.listen()
        else:
            # otherwise call the send method
            self.send()


def main():
    # Using argparse module to create a CLI
    parser = argparse.ArgumentParser(
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
