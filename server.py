import socket

def start_server(host='127.0.0.1', port=65432):
    """Start a basic TCP server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Allow reusing the socket address
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind server to host and port
        server_socket.bind((host, port))
        server_socket.listen()

        print(f"Server running on {host}:{port}... Waiting for a connection.")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f"Received from client: {data.decode()}")
                    conn.sendall(b"Hello from server!")

if __name__ == "__main__":
    start_server()
