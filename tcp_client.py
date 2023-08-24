import socket


target_host = "0.0.0.0"
target_port = 9998

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# AF_INET -> Indicates that we'll use a standard IPv4 address or hostname

# SOCK_STREAM -> Indicates that this will be a TCP client

# connect the client
client.connect((target_host, target_port))

# send some data
client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

# receive some data
response = client.recv(4096)

print(response.decode())
client.close()
