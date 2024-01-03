import time

from server_socket import Server

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
