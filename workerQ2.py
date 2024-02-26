import socket
import pickle

def square(x):
    return x ** 2

def handle_task(client_socket):
    try:
        data = client_socket.recv(4096)
        task_data = pickle.loads(data)

        task = task_data['task']
        args = task_data['args']
        kwargs = task_data['kwargs']

        result = task(*args, **kwargs)

        result_data = pickle.dumps(result)
        client_socket.sendall(result_data)

    except Exception as e:
        print("Error:", e)

    finally:
        client_socket.close()

def start_worker():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 9999))
        server_socket.listen(5)
        print("Worker node listening...")

        while True:
            client_socket, _ = server_socket.accept()
            print("Task received from client.")
            handle_task(client_socket)

    except Exception as e:
        print("Error:", e)

    finally:
        server_socket.close()

if __name__ == "__main__":
    start_worker()
