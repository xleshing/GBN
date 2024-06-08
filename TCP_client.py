import socket

def send_image(filename, server_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    
    with open(filename, 'rb') as f:
        data = f.read()
        sock.sendall(data)
    
    print(f"Sent image {filename}")
    sock.close()

send_image('img.png', ('localhost', 10000))
