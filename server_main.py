import socket

host = '127.0.0.1'  # 伺服器的IP地址
port = 555
address = (host, port)

socket01 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 使用UDP

window_size = 4  # GBN窗口大小
base = 0
next_seq_num = 0
expected_seq_num = 0

socket01.bind(address)
print('啟動Socket')

def receive_data(conn):
    global base, expected_seq_num
    while True:
        data, addr = conn.recvfrom(1024)
        seq_num = int(data[:3])  # 從封包中提取序列號
        payload = data[3:]  # 從封包中提取資料
        print(f"接收到序列號為{seq_num}的封包")
        if seq_num == expected_seq_num:
            conn.sendto(str(seq_num).encode(), addr)  # 對已收到的封包發送確認回應
            expected_seq_num += 1
            if expected_seq_num == base + window_size:
                base += window_size
                print("基準更新為", base)
        else:
            print(f"接收到序列號為{seq_num}的封包，但序列號與預期不符。將丟棄。")

        if payload == b'':  # 檢查是否收到結束傳輸的封包
            break

    print('傳輸結束')

print('等待連接...')
while True:
    data, addr = socket01.recvfrom(1024)  # 從客戶端接收請求
    if data == b'request':
        print('已連接至', addr)
        receive_data(socket01)
        break

socket01.close()
print('伺服器已關閉')
