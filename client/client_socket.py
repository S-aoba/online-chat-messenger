import socket

class Client:
  MIN_USERNAME_SIZE = 1
  MAX_USERNAME_SIZE = 25
  def __init__(self) -> None:
    self.server_address = '0.0.0.0'
    self.tcp_server_port = 9001
    self.udp_server_port = 9002

    self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    self.username = ''
    self.username_size = 0

    self.udp_sock.bind((self.server_address, 0))

  def start(self):
    # usernameを入力させる
    self.input_username()
    # tcp接続をする


  def input_username(self):
    while True:
      username = input('ユーザーネーム: ')
      if len(username) < self.MIN_USERNAME_SIZE or len(username) > self.MAX_USERNAME_SIZE:
        print('ユーザーネームは、{}文字以上{}文字以下にしてください。'.format(self.MIN_USERNAME_SIZE, self.MAX_USERNAME_SIZE))
        continue

      self.username = username
      self.username_size = len(username)
      break

  def connect_tcp_server(self):
    self.tcp_sock.connect((self.server_address, self.tcp_server_port))
    


