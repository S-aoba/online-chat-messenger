import socket
import threading
import time
import sys
class Server:
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



  def server_stop(self):
    print('サーバーを終了します')
    self.tcp_sock.close()
    sys.exit()

def main():
    server = Server()
    server.start()

    try:
      while True:
         time.sleep(1)
    except KeyboardInterrupt:
      server.server_stop()


if __name__ == "__main__":
    main()
