import socket
import pickle

def square(x):
    return x ** 2

def send_task(task, *args, **kwargs):
    try:
        task_data = {
            'task': task,
            'args': args,
            'kwargs': kwargs
        }

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)  # Set a timeout of 5 seconds
        client_socket.connect(('localhost', 9999))

        data = pickle.dumps(task_data)
        client_socket.sendall(data)

        result = client_socket.recv(4096)
        result = pickle.loads(result)
        print("Result:", result)

    except socket.timeout:
        print("Error: Socket timeout occurred. Server might be unresponsive.")
    except ConnectionRefusedError:
        print("Error: Connection refused. Server is not running or is unreachable.")
    except Exception as e:
        print("Error:", e)

    finally:
        client_socket.close()

if __name__ == "__main__":
    print("Task: Square of any value")
    var = int(input("Enter a number to square: "))
    send_task(square, var)
