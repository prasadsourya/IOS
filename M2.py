import mimetypes
import os.path
import socket


class HTTPServer:
    def __init__(self, IP, port):
        super().__init__()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as self.s:
            self.s.bind((IP, port))
            self.s.listen()
            while True:
                conn, addr = self.s.accept()
                with conn:
                    print('Connected by', addr)
                    # TODO read the request and extract the URI

                    # TODO update the parameter with the request URI
                    ur = conn.recv(1024)
                    # print(ur.decode())
                    uri = ur.decode().splitlines()[
                        0].split("/")[1].split(" ")[0]
                    code, c_type, c_length, data = self.get_data(uri)
                    response = self.response_headers(
                        code, c_type, c_length).encode() + data
                    conn.sendall(response)
                    conn.close()

    def get_data(self, uri):
        '''
            TODO: This function has to be updated for M2
        '''
        if len(uri) == 0:
            data = "<h1>Webserver Under construction</h1>"
            return 200, "text/html", len(data), data.encode()
        p = os.getcwd() + "/www/" + uri
        if os.path.isfile(p):
            p = open(p, 'rb')
            data = p.read()
            return 200, mimetypes.MimeTypes().guess_type(uri)[0], len(data), data
        else:
            data = "<h1>File Not Found</h1>".encode()
            return 404, "text/html", len(data), data

    def response_headers(self, status_code, content_type, length):
        line = "\n"

        # TODO update this dictionary for 404 status codes
        response_code = {200: "200 OK", 404: "404 Not Found"}

        headers = ""
        headers += "HTTP/1.1 " + response_code[status_code] + line
        headers += "Content-Type: " + content_type + line
        headers += "Content-Length: " + str(length) + line
        headers += "Connection: close" + line
        headers += line
        return headers


def main():
    # test harness checks for your web server on the localhost and on port 8888
    # do not change the host and port
    # you can change  the HTTPServer object if you are not following OOP
    HTTPServer('127.0.0.1', 8888)


if __name__ == "__main__":
    main()