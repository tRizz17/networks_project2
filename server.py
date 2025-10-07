from urllib.parse import urlparse
import socket
import os
import argparse
import mimetypes


def splitAndParse(header):
    first_line = header[0].split()
    parsed = urlparse(first_line[1])
    full_path = parsed.path
    method = first_line[0]
    version = first_line[2]
    file_name = os.path.split(full_path)[-1]
    
    return method, file_name, version


def WebServer(port):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen()
    while True:
        print("Listening for incoming connections...\r\n")
        new_conn = s.accept()
        client_addr = new_conn[1][0]
        # print(f"IP Address: {client_addr}")
        new_socket = new_conn[0]
        buffer = b""
        while True:
            request_data = new_socket.recv(1024)
            buffer += request_data
            if b"\r\n\r\n" in buffer:
                decoded_buffer = buffer.decode("ISO-8859-1")
                print(decoded_buffer)
                header = decoded_buffer.split("\r\n")
                method, file_name, version = splitAndParse(header)
                mimetype, _ = mimetypes.guess_type(file_name)

                if mimetype is None:
                    mimetype = "application/octet-stream"

                try:
                    with open(file_name, "rb") as fp:
                        data = fp.read()
                        content_length = len(data)
                        response = (
                            f"HTTP/1.1 200 OK\r\n"
                            f"Content-Type: {mimetype}\r\n"
                            f"Content-Length: {content_length}\r\n"
                            f"Connection: close\r\n\r\n"
                        ).encode("ISO-8859-1")
                        new_socket.sendall(response + data)
                        new_socket.close()

                except FileNotFoundError:
                    payload = "404 Not Found"
                    content_length = len(payload)
                    not_found_response = (
                        "HTTP/1.1 404 Not Found\r\n"
                        "Content-Type: text/plain\r\n"
                        f"Content-Length: {content_length}\r\n"
                        f"Connection: close\r\n\r\n"
                    ).encode("ISO-8859-1")
                    new_socket.sendall(not_found_response + payload.encode("ISO-8859-1"))
                    new_socket.close()
                    break

                break   

parser = argparse.ArgumentParser(description="Specify a port number if you wish")
parser.add_argument("port", nargs="?", type=int, default=28333, help="Enter a valid port number")
args = parser.parse_args()

if __name__ == "__main__":
    WebServer(args.port)