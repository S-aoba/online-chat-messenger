import json
import socket
import struct
import threading
import sys

class Server:
  MAX_HEADER_BYTE_SIZE = 32
  def __init__(self) -> None:
    self.server_address = '0.0.0.0'
    self.tcp_server_port = 9001
    self.udp_server_port = 9002

    self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    self.tcp_sock.bind((self.server_address, self.tcp_server_port))
    self.udp_sock.bind((self.server_address, self.udp_server_port))

  def start(self):
    thread_tcp_socket = threading.Thread(target=self.waiting_tcp_client, daemon=True)
    thread_tcp_socket.start()

  def waiting_tcp_client(self):
    self.tcp_sock.listen(1)
    print('クライアントの接続を待っています。')

    while True:
      client_socket, client_address = self.tcp_sock.accept()
      print(f"クライアントが接続されました。アドレス: {client_address}")

      # クライアントからの情報(チャットルーム名や作成又は参加の有無等)を別スレッドで関数を動かし受け取る
      chatroom_name, username, operation_code, state, operation_payload = self.receive_tcp_data(client_socket)

      print(state)


  def receive_tcp_data(self, client_socket: socket.socket):
    header = client_socket.recv(self.MAX_HEADER_BYTE_SIZE)
    # バイナリ形式で受け取ったヘッダー情報をunpackして取得する
    chatroom_name_size, operation_code, state, operation_payload_size = struct.unpack('! B B B 29s', header)

    chatroom_name = client_socket.recv(chatroom_name_size).decode('utf-8')

    operation_payload = client_socket.recv(int.from_bytes(operation_payload_size, 'big'))

    operation_payload = json.loads(operation_payload)

    username = operation_payload['username']

    return chatroom_name, username, operation_code, state, operation_payload








  def server_stop(self):
    print('サーバーを終了します')
    self.tcp_sock.close()
    sys.exit()


