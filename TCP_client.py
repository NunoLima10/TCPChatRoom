from src.client_chat import ClientChat

import socket
import threading

BUFFER_SIZE = 1024

class TCPClient:
    def __init__(self) -> None:
        self.online = True
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = input("Enter your nickname: ")

    def connect(self, host: str, port: int) -> None:
        self.client_socket.connect((host,port))
    
    def receive_message(self) -> None:
        while self.online:
            try:
                message = self.client_socket.recv(BUFFER_SIZE).decode()
                if message == "NICK":
                    self.client_socket.send(self.nickname.encode())
                else:
                    ClientChat.notify_new_message(message)
            except:
                self.close()

    def write_message(self) -> None:
        while self.online:
            try:
                message = ClientChat.client_message(self.nickname,input(''))
                self.client_socket.send(message.encode())
            except KeyboardInterrupt:
                self.close()
            except EOFError:
                self.close()

    def start(self) -> None:
        receive_tread = threading.Thread(target=self.receive_message)
        receive_tread.start()

        write_tread = threading.Thread(target=self.write_message)
        write_tread.start()
    
    def close(self) -> None:
        if self.online:
            ClientChat.notify_connection_lost()
            self.online = False
            self.client_socket.close()
            exit()

client =  TCPClient()
client.connect("127.0.0.1",3000)
client.start()