import socket
import cv2
import numpy as np
import threading

def convert_to_temperature(image):
    intensity_values = image[:, :, 0]  
    average_intensity = np.mean(intensity_values)

    temperature = 20.0 + 0.1 * average_intensity

    return temperature

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(921600) 
            if not data:
                break

            expected_size = 640 * 480 * 3
            if len(data) != expected_size:
                print(f"Received data size does not match expected size. Skipping frame.")
                continue

            frame = np.frombuffer(data, dtype=np.uint8).reshape((480, 640, 3))

            temperature = convert_to_temperature(frame)

            client_socket.sendall(str(temperature).encode())

    except Exception as e:
        print(f"Error handling client: {e}")

    finally:
        client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 12345))
server_socket.listen(5)

print("Server listening on port 12345")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
