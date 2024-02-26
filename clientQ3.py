import socket
import threading
import pickle

class ChatClient:
    def __init__(self):
        self.host = 'localhost'
        self.port = 9999
        self.username = input("Enter your username: ")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.socket.connect((self.host, self.port))
        print("Connected to server")
        threading.Thread(target=self.receive_messages).start()
        print("You can start texting below\n Note: Your message will be displayed to all the user conectefd to the server")
        self.send_messages()

    def send_messages(self):
        try:
            while True:
                message = input()
                if message.lower() == 'exit':
                    break
                data = {'username': self.username, 'message': message}
                
                self.socket.sendall(pickle.dumps(data))
        except Exception as e:
            print("Error:", e)
        finally:
            self.socket.close()

    def receive_messages(self):
        try:
            while True:
                data = self.socket.recv(4096)
                if not data:
                    break
                message = pickle.loads(data)
                print(f"{message['username']}: {message['message']}")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    chat_client = ChatClient()
