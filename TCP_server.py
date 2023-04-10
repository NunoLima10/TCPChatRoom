from src.server_chat import ServerChat

import socket
import threading

BUFFER_SIZE = 1024

class TCPServer:
    def __init__(self, host: str = "127.0.0.1", port : int = 3000 ) -> None:
        self.host = host 
        self.port = port
        self.clients: list[socket.socket] = []
        self.clients_nickname: list[str] = []
        self.online = True 

        #create an bind socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))

    def get_client_nickname(self, client: socket.socket) -> str:
        client.send('NICK'.encode())
        nickname = client.recv(BUFFER_SIZE)
        return nickname.decode()

    def broadcast_message(self, message: bytes, sender_client: socket.socket = None) -> None: 
        for client in self.clients:
            if client != sender_client:
                client.send(message)
    
    def broadcast_server_message(self, message: bytes) -> None: 
        for client in self.clients:
            if client is not None:
                client.send(message)

    def start(self) -> None:
        ServerChat.notify_server_start(self.host, self.port)
        self.server_socket.listen()

        while self.online:
            client, address = self.server_socket.accept()
            nickname = self.get_client_nickname(client)

            self.clients.append(client)
            self.clients_nickname.append(nickname)

            server_message = ServerChat.notify_new_client(nickname, address)
            self.broadcast_server_message(server_message.encode())

            thread = threading.Thread(target=self.handle_client,args=(client,))
            thread.start()
            
           
    def handle_client(self, client: socket.socket) -> None:
        while True:
            try:
                message = client.recv(BUFFER_SIZE)
                self.broadcast_message(message, client)
            except:
                break

        client.close()
        client_index = self.clients.index(client)
        server_message = ServerChat.notify_client_left(self.clients_nickname[client_index])
        del self.clients[client_index]
        del self.clients_nickname[client_index]
        self.broadcast_server_message(server_message.encode())
  
server = TCPServer()
server.start()