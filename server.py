from urllib.parse import urlparse
import os
import argparse

def extractSchemeAndPath(url):
    url = urlparse(url)
    scheme = url.scheme
    return (url.scheme, url.path)


def getMIMEType(path):
    split_the_path = os.path.split(path)
    get_mime = os.path.splitext(split_the_path[-1])
    mime = get_mime[-1]
    return mime


def WebServer(port):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen()
    while True:
        print("Listening for incoming connections...")
        new_conn = s.accept()
        client_addr = new_conn[1][0]
        print(f"IP Address: {client_addr}")
        new_socket = new_conn[0]
        buffer = ""
        while True:
            request_data = new_socket.recv(1024).decode("ISO-8859-1")
            buffer += request_data
            if "\r\n\r\n" in buffer:
                print(buffer)
                break



mapping = {
    "html": "text/html",
    "txt": "txt/plain"
}

parser = argparse.ArgumentParser(description="Specify a port number if you wish")
parser.add_argument("port", nargs="?", type=int, default=28333, help="Enter a valid port number")
args = parser.parse_args()

if __name__ == "__main__":
    WebServer.py(port)

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
