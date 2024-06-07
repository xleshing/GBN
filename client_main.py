import socket
import time

host = '127.0.0.1'  # 伺服器的IP地址
port = 555
address = (host, port)

socket02 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 使用UDP

window_size = 4  # GBN窗口大小
base = 0
next_seq_num = 0
expected_ack_num = 0
timeout = 2  # 超時時間（秒）

def send_packet(packet, seq_num):
    socket02.sendto(packet, address)
    print(f"已發送序列號為{seq_num}的封包")

def receive_ack():
    global base, next_seq_num
    while True:
        try:
            socket02.settimeout(timeout)
            ack, _ = socket02.recvfrom(1024)
            ack_num = int(ack.decode())  # 解析ACK中的序列號
            print(f"接收到序列號為{ack_num}的ACK")
            if ack_num == base:
                base += 1
                if base == next_seq_num:
                    socket02.settimeout(None)  # 取消超時
                else:
                    socket02.settimeout(timeout)  # 重新設置超時
            else:
                socket02.settimeout(timeout)  # 重新設置超時
        except socket.timeout:
            print(f"超時，重新傳送序列號為{base}及之後的封包")
            for i in range(base, next_seq_num):
                send_packet(packets[i], i)

# 創建封包
packets = []
with open("img.png", "rb") as imgFile:
    while True:
        imgData = imgFile.read(512)
        if not imgData:
            break  # 讀完檔案結束迴圈
        packet = str(next_seq_num).zfill(3).encode() + imgData
        packets.append(packet)
        next_seq_num += 1

# 開始傳輸
print('開始傳送影像')
while base < len(packets):
    for i in range(base, min(next_seq_num, len(packets))):
        send_packet(packets[i], i)
    receive_ack()

socket02.close()
print('傳輸結束')
