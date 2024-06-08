import socket
import random

host = '127.0.0.1'
port = 5555
address = (host, port)

socket02 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# GBN
window_size = 5
base = 0
next_seq_num = 0
timeout = 0.2
packet_loss_rate = 0.05  # 丢包率

def send_packet(packet, seq_num):
    if random.random() > packet_loss_rate:  # 模擬丢包
        socket02.sendto(packet, address)
        print(f"Sent packet{seq_num}")
    else:
        print(f"Dropped packet{seq_num}")

def receive_ack():
    global base, next_seq_num
    try:
        socket02.settimeout(timeout)
        ack, _ = socket02.recvfrom(1024)
        ack_num = int(ack.decode())  # 解析ACK中的序號
        print(f"Received ACK{ack_num}")
        if base <= ack_num < next_seq_num:
            base = ack_num + 1
        else:
            print(f"ACK error, resend packets{base}")
            for i in range(base, next_seq_num):
                send_packet(packets[i], i)
    except socket.timeout:
        print(f"Timeout, resend packets{base}")
        for i in range(base, next_seq_num):
            send_packet(packets[i], i)


packets = []
with open("img.png", "rb") as imgFile:
    while True:
        imgData = imgFile.read(512)
        if not imgData:
            break
        packet = str(next_seq_num).zfill(10).encode() + imgData
        packets.append(packet)
        next_seq_num += 1


next_seq_num = 0


send_packet(str("request").encode().zfill(10), "request")


print('Starting image transfer')
while base < len(packets):
    while next_seq_num < base + window_size and next_seq_num < len(packets):
        send_packet(packets[next_seq_num], next_seq_num)
        next_seq_num += 1
    receive_ack()


send_packet(str("END").encode().zfill(10), "END")

socket02.close()
print('Transfer complete')
