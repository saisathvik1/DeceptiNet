import socket
import datetime

def ssh_honeypot():
    host = "0.0.0.0"
    port = 22

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"SSH Honeypot: Listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address[0]}:{client_address[1]}")

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{current_time}] Connection from {client_address[0]}:{client_address[1]}\n"

        with open("ssh_honeypot.log", "a") as log_file:
            log_file.write(log_message)

        client_socket.recv(1024)  # Consume the initial received data

        client_socket.close()

ssh_honeypot()
