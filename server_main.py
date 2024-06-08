import socket

host = '127.0.0.1'
port = 5555
address = (host, port)

socket01 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# GBN
window_size = 4
base = 0
expected_seq_num = 0
send_incorrect_ACK = False

socket01.bind(address)
print('Socket started')


def receive_data(conn, filename):
    global base, expected_seq_num, send_incorrect_ACK
    with open(filename, 'wb') as f:
        while True:
            data, addr = conn.recvfrom(1024)

            if data == b'END'.zfill(10):
                print('Done')
                break

            seq_num = int(data[:10])  # 提取序號
            payload = data[10:]  # 提取DATA
            print(f"Received packet{seq_num}")

            if seq_num == expected_seq_num:
                f.write(payload)
                conn.sendto(str(seq_num).zfill(10).encode(), addr)  # 發送ACK
                expected_seq_num += 1
                print(f"Ack packet{seq_num}")
                send_incorrect_ACK = False
            else:
                if not send_incorrect_ACK:
                    conn.sendto(str(expected_seq_num - 1).zfill(10).encode(), addr)  # 發送ACK
                    send_incorrect_ACK = True
                    print(f"Received packet{seq_num}, doesn't match, resend Ack packet{expected_seq_num - 1}")


print('Waiting for connection...')
while True:
    data, addr = socket01.recvfrom(1024)
    if data == b'request'.zfill(10):
        print('Connected to', addr)
        receive_data(socket01, 'received_image.png')
        break

socket01.close()
print('Server closed')
