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
        buffer = ""
        while True:
            request_data = new_socket.recv(1024).decode("ISO-8859-1")
            buffer += request_data
            if "\r\n\r\n" in buffer:
                print(buffer)
                header = buffer.split("\r\n")
                method, file_name, version = splitAndParse(header)
                mimetype, _ = mimetypes.guess_type(file_name)
                if mimetype is None:
                    mimetype = "application/octet-stream"
                print(method, file_name, version, mimetype)
                try:
                    with open(file_name, "rb") as fp:
                        data = fp.read()
                        print(data)
                        content_length = data.length()
                        response = (
                            f"HTTP/1.1 200 OK\r\n"
                            f"Content-Type: {mimetype}\r\n"
                            f"Content-Length: {content_length}\r\n"
                            f"Connection: close\r\n\r\n{data}\r\n\r\n"
                        )
                        new_socket.sendall(response.encode("ISO-8859-1"))
                        new_socket.close()
                except:
                    not_found_response = (
                        "HTTP/1.1 404 Not Found\r\n"
                        "Content-Type: text/plain\r\n"
                        "Content-Length: 13\r\n"
                        "Connection: close\r\n\r\n404 Not Found"
                    )
                    new_socket.sendall(not_found_response.encode("ISO-8859-1"))
                    new_socket.close()
                    break

                break   

parser = argparse.ArgumentParser(description="Specify a port number if you wish")
parser.add_argument("port", nargs="?", type=int, default=28333, help="Enter a valid port number")
args = parser.parse_args()

if __name__ == "__main__":
    WebServer(args.port)

# Parse that request header to get the file name.
# Strip the path off for security reasons.
# Read the data from the named file.
# Determine the type of data in the file, HTML or text.
# Build an HTTP response packet with the file data in the payload.
# Send that HTTP response back to the client.

# Response ->
# HTTP/1.1 200 OK
# Content-Type: text/html
# Content-Length: 373
# Connection: close

# <!DOCtype html>

# <html>
# <head>
# ...



# if extension in mapping:
#     else:
#         #application/octet-stream

# key = "gif"

# mimeType = mapping.get(key)

# if mimeType is None:
#     #application/octet-stream

