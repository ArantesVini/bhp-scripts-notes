import socket

target_host = "127.0.0.1"
target_port = 1997

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Here whe change the socket type to SOCK_DGRAM, which stands for datagram


# Send some data
client.sendto(b"AAABBBCCC", (target_host, target_port))
# As UDP is a connectionless protocol, we don't need to call the connect() method

# Receive some data
data, addr = client.recvfrom(4096)
print(data.decode())
client.close()
