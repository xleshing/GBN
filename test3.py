import socket

def send_image(filename, server_address):
    # 設置TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    
    # 讀取圖片並傳送
    with open(filename, 'rb') as f:
        data = f.read()
        sock.sendall(data)
    
    print(f"Sent image {filename}")
    sock.close()

# 示例圖片發送
send_image('img.png', ('localhost', 10000))
