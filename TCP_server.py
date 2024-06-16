import socket

def receive_image(save_as, server_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen(1)
    
    print("Waiting for a TCP connection...")
    connection, client_address = sock.accept()
    
    with open(save_as, 'wb') as f:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            f.write(data)
    
    print(f"Received image and saved as {save_as}")
    connection.close()
    sock.close()

receive_image('received_TCP.jpg', ('localhost', 10000))
