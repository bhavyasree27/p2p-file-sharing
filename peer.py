import socket
import os
from utils import progress_bar

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(1)
        print(f"[LISTENING] Server running on {self.host}:{self.port}")

        conn, addr = server.accept()
        print(f"[CONNECTED] Client connected from {addr}")

        filename = conn.recv(1024).decode()
        filesize = int(conn.recv(1024).decode())
        print(f"[RECEIVING] File: {filename} ({filesize} bytes)")

        with open("received_" + filename, "wb") as f:
            received = 0
            while received < filesize:
                bytes_read = conn.recv(1024)
                if not bytes_read:
                    break
                f.write(bytes_read)
                received += len(bytes_read)
                progress_bar(received, filesize)

        print("\n✅ File received successfully.")
        conn.close()
        server.close()

    def send_file(self, filepath):
        if not os.path.exists(filepath):
            print("File not found.")
            return

        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))

        client.send(filename.encode())
        client.recv(1)
        client.send(str(filesize).encode())
        client.recv(1)

        print(f"[SENDING] Sending {filename} ({filesize} bytes)...")
        with open(filepath, "rb") as f:
            sent = 0
            while True:
                bytes_read = f.read(1024)
                if not bytes_read:
                    break
                client.sendall(bytes_read)
                sent += len(bytes_read)
                progress_bar(sent, filesize)

        print("\n✅ File sent successfully.")
        client.close()
