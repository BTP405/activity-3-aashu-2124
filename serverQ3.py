import socket
import threading
import pickle

class ChatServer:
    def __init__(self):
        self.host = 'localhost'
        self.port = 9999
        self.clients = []
        self.lock = threading.Lock()
        self.running = True

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Server listening on port", self.port)
        
        self.server_thread = threading.Thread(target=self.accept_clients)
        self.server_thread.start()

    def accept_clients(self):
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address}")
                self.clients.append(client_socket)
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            except Exception as e:
                print("Error accepting client:", e)
                break

    def stop(self):
        self.running = False
        self.server_socket.close()
        for client_socket in self.clients:
            client_socket.close()

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                message = pickle.loads(data)
                self.broadcast(data, client_socket)
        except Exception as e:
            print("Error:", e)
        finally:
            self.remove_client(client_socket)

    def broadcast(self, data, sender_socket):
        with self.lock:
            for client in self.clients:
                if client != sender_socket:
                    try:
                        client.sendall(data)
                    except Exception as e:
                        print("Error broadcasting to client:", e)
                        self.remove_client(client)

    def remove_client(self, client_socket):
        with self.lock:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
                client_socket.close()
                print("Client disconnected")

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down server...")
        chat_server.stop()
