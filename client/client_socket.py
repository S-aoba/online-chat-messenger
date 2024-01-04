import socket
import json
import struct

from constants.operation import Operation


class Client:
  MIN_USERNAME_SIZE = 1
  MAX_USERNAME_SIZE = 25

  MIN_CHATROOM_NAME_SIZE = 1
  MAX_CHATROOM_NAME_SIZE = 25

  def __init__(self) -> None:
    self.server_address = '0.0.0.0'
    self.tcp_server_port = 9001
    self.udp_server_port = 9002

    self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    self.username = ''
    self.username_size = 0

    # チャットルームを1.新規で立てるか、2.参加するかを表すメンバ変数(1 or 2)
    self.operation_code = 0
    self.state = 0
    self.chatroom_name = ''
    self.password = ''

    self.udp_sock.bind((self.server_address, 0))

  def start(self):
    # usernameを入力させる
    self.input_username()
    # tcp接続をする
    self.tcp_sock.connect((self.server_address, self.tcp_server_port))
    # serverに渡すpayloadを作成
    operation_payload = self.create_operation_payload()

    custom_tcp_request: bytes = self.create_tcp_protocol(operation_payload)

    self.tcp_sock.sendall(custom_tcp_request)

  def input_username(self):
    while True:
      username = input('ユーザーネーム: ')
      if len(username) < self.MIN_USERNAME_SIZE or len(username) > self.MAX_USERNAME_SIZE:
        print('ユーザーネームは、{}文字以上{}文字以下にしてください。'.format(self.MIN_USERNAME_SIZE, self.MAX_USERNAME_SIZE))
        continue

      self.username = username
      self.username_size = len(username)
      break

  def create_operation_payload(self):
    self.operation_code = self.prompt_create_or_join_chatroom()

    self.chatroom_name = self.prompt_chatroom_name()

    self.password = self.prompt_password()

    operation_payload = {
      'username': self.username,
      'ip': self.server_address,
      'port': self.tcp_server_port,
      'password': self.password
    }

    return operation_payload

  def prompt_create_or_join_chatroom(self):
    while True:
      try:
        operation_code_str = input('1.新しい部屋を作る 2.参加する (1/2): ')
        operation_code = int(operation_code_str)

        if operation_code in [Operation.CREATE_CHATROOM.value, Operation.JOIN_CHATROOM.value]:
          return operation_code
        print('1又は2のどちらかを入力してください')

      except ValueError:
        print('1又は2のどちらかを入力してください')

  def prompt_chatroom_name(self):
    while True:
      chatroom_name = input('部屋名: ')

      if len(chatroom_name) < self.MIN_CHATROOM_NAME_SIZE or self.MAX_CHATROOM_NAME_SIZE < len(chatroom_name):
        print('{}文字以上{}文字以下で入力して下さい'.format(self.MIN_CHATROOM_NAME_SIZE, self.MAX_CHATROOM_NAME_SIZE))

      else:
        return chatroom_name

  def prompt_password(self):
    while True:
      password = input('パスワード(6文字以上): ')

      if len(password) < 6:
        print('6文字以上入力して下さい')
      # 数値があるかどうか
      elif not any(char.isdigit() for char in password):
        print("パスワードには必ず数値を含んで下さい")
      elif not any(char.isalpha() for char in password):
        print('パスワードには必ずアルファベットを1文字以上含んで下さい')
      else:
        return password

  def create_tcp_protocol(self, operation_payload: dict) -> bytes:
    operation_payload_byte = json.dumps(operation_payload).encode()
    operation_payload_size_byte = len(operation_payload_byte).to_bytes(29, 'big')

    header = struct.pack('!B B B 29s', len(self.chatroom_name), self.operation_code, self.state, operation_payload_size_byte)
    body = self.chatroom_name.encode() + operation_payload_byte

    return header + body
