import socket

def ftp_honeypot():
    host = "0.0.0.0"  # Listen on all available interfaces
    port = 21         # FTP port, port can be changed.

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen(5)

        print(f"FTP Honeypot: Listening on {host}:{port}")

        while True:
            client_socket, client_address = server.accept()
            print(f"Connection from {client_address[0]}:{client_address[1]}")

            client_socket.send(b"220 (vsFTPd 2.3.4)\r\n")  # It currently shows as VSFTPD 2.3.4, but it can be changed.

            while True:
                data = client_socket.recv(1024).decode().strip()

                if not data:
                    break

                print(f"Received: {data}")

                if "USER anonymous" in data:
                    client_socket.send(b"331 Please specify the password.\r\n")
                elif "PASS" in data:
                    client_socket.send(b"230 Login successful.\r\n")

                    with open("ftp_log.txt", "a") as log_file:
                        log_file.write(f"Connection from {client_address[0]}:{client_address[1]} - Anonymous login\n")

                elif "QUIT" in data:
                    client_socket.send(b"221 Goodbye.\r\n")
                    client_socket.close()
                    break
                else:
                    client_socket.send(b"530 Login incorrect.\r\n")

            client_socket.close()

if __name__ == "__main__":
    ftp_honeypot()
