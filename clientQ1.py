import socket
import pickle

def send_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            file_data = {
                'name': file_path,
                'data': file.read()
            }

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 9999))

        data = pickle.dumps(file_data)  
        client_socket.sendall(data)

        print("File sent successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        client_socket.close()

if __name__ == "__main__":
    file_path = input("Enter the file path: ")
    send_file(file_path)
