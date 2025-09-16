from peer import Peer

if __name__ == "__main__":
    mode = input("Enter mode (server/client): ").strip().lower()
    host = "0.0.0.0" if mode == "server" else input("Enter server IP (default 127.0.0.1): ") or "127.0.0.1"
    port = 5001

    peer = Peer(host, port)

    if mode == "server":
        peer.start_server()
    elif mode == "client":
        filepath = input("Enter path to file to send: ").strip()
        peer.send_file(filepath)
    else:
        print("Invalid mode. Choose server or client.")
