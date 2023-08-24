import socket
import threading


IP = "0.0.0.0"
PORT = 9998

def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f"[*] Received: {request.decode('utf-8')}")
        sock.send(b"ACK")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # IP and PORT to server listen on
    server.bind((IP, PORT))
    # Tell to the server start listening with a maximum backlog of connections set to 5
    server.listen(5)
    print(f"[*] Listening on {IP}:{PORT}")
    while True:
        # When a client connects, we receive the client socket into the client variable,
        #  and the remote connection details into the address variable
        client, address = server.accept()
        print(f"[*] Accepted connection from {address[0]}:{address[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        # Start the thread to handle the client connection
        client_handler.start()

if __name__ == "__main__":
    main()