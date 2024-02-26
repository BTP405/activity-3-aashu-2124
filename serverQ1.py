import socket
import pickle
import os

def receive_file(save_dir):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 9999))
        server_socket.listen(5)
        print("Server listening...")

        while True:
            client_socket, address = server_socket.accept()
            print(f"Connection from {address} has been established.")

            data = client_socket.recv(4096)
            if not data:
                break

            file_data = pickle.loads(data)
            file_name = os.path.basename(file_data['name'])
            save_path = os.path.join(save_dir, file_name)

            with open(save_path, 'wb') as file:
                file.write(file_data['data'])

            print(f"File saved to: {save_path}")

            client_socket.close()

    except Exception as e:
        print("Error:", e)

    finally:
        server_socket.close()

if __name__ == "__main__":
    receive_file("received_files")
