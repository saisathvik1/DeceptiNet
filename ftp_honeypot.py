import socket
import datetime
import os

def ftp_honeypot():
    host = "0.0.0.0"  # Listen on all available interfaces
    port = 21         # FTP port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen(5)

        print(f"FTP Honeypot: Listening on {host}:{port}")

        while True:
            client_socket, client_address = server.accept()
            print(f"Connection from {client_address[0]}:{client_address[1]}")

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{current_time}] Connection from {client_address[0]}:{client_address[1]}"

            client_socket.send(b"220 (vsFTPd 2.3.4)\r\n")  # Modify the banner here

            while True:
                data = client_socket.recv(1024).decode().strip()

                if not data:
                    break

                print(f"Received: {data}")
                log_message += f"\nReceived: {data}"

                if "USER anonymous" in data:
                    client_socket.send(b"331 Please specify the password.\r\n")
                elif "PASS" in data:
                    client_socket.send(b"230 Login successful.\r\n")

                # ... rest of your code ...

            # Log every connection attempt
            if not os.path.exists("ftp_log.log"):
                with open("ftp_log.log", "w") as log_file:
                    pass  # Create an empty file

            with open("ftp_log.log", "a") as log_file:
                log_file.write(f"{log_message}\n")

            client_socket.close()

if __name__ == "__main__":
    ftp_honeypot()
