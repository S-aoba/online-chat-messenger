import socket

class Client:
  def __init__(self) -> None:
    self.server_address = '0.0.0.0'
    self.tcp_server_port = 9001
    self.udp_server_port = 9002

    self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    self.udp_sock.bind((self.server_address, 0))

  def start(self):
    self.tcp_sock.connect((self.server_address, self.tcp_server_port))

def main():
  client = Client()
  client.start()

if __name__ == "__main__":
  main()
