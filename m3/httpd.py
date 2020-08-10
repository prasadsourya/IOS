'''
    Disclaimer
    tiny httpd is a web server program for instructional purposes only
    It is not intended to be used as a production quality web server
    as it does not fully in compliance with the 
    HTTP RFC https://tools.ietf.org/html/rfc2616

    This task is designed by Praveen Garimella and is to be used
    as part of the Learning by Doing, Project Based Course on Operating Systems
    Write to pg@fju.us for any questions or comments
'''

'''
    == Task 2 ==
    This file has the solution for M1 and the description for M2.
    Review this solution before you start implementing the M2.
    If you don't like our solution for M1 then
    tell us why so that we can improve it.

    In the M2 you have to write code to handle http requests for static content.
    Web servers maintain static content in a directory called document root.
    We have provided you with a directory with the name www.
    This directory has some html files and images.
    A web server may receive a request to access one of these files.

    When such a request is received you have to parse the HTTP request
    and extract the name of the file in the request aka Uniform Resourse Indicator    
    Learn the format of the http requests from the tutorial given below.
    https://www.tutorialspoint.com/http/http_requests.htm

    After extracting the URI,
    check if the file exists in the document root directory i.e., www

    If it exists, you have to read the file contents as the response data.
    If not you have to send a 404 file not found response.

    Construct the http response by invoking response_headers method
    This method is provided in the HTTPServer class
    Passing the appropriate response code, content type and length to the method
    
    A tricky part to the response construction is to identify the content type.
    Set the content type text/html for files that end with the extension .html
    
    What would be the content type for images? Review the link below.
    https://www.iana.org/assignments/media-types/media-types.xhtml#image

    How do we figure out the content subtype of an image?
    Explore the use of the library mimetype in python.
    https://www.tutorialspoint.com/How-to-find-the-mime-type-of-a-file-in-Python

    @credits Sudheer
'''

import socket
import os.path
import mimetypes

class HTTPServer:
    def __init__(self, IP, port):
        super().__init__()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as self.s:
            self.s.bind((IP, port))
            self.s.listen()
            while True:
                conn, addr = self.s.accept()
                with conn:
                    # print('Connected by', addr)
                    # TODO read the request and extract the URI
                    path = conn.recv(1024).decode()
                    # TODO update the parameter with the request URI
                    # print("here", path)
                    path = path.splitlines()[0]
                    # print(path)
                    uri = path.split(" ")[1]
                    code, c_type, c_length, data = self.get_data(uri)
                    response = self.response_headers(code, c_type, c_length).encode() + data
                    conn.sendall(response)
                    conn.close()
    
    def get_data(self, uri):
        '''
            TODO: This function has to be updated for M2
        '''
        print("here",uri)
        p = os.getcwd() + uri
        if os.path.isdir(p):
            data = ''
            file_list = os.listdir(p)
            print(file_list)
            for each in file_list:
                if uri == '/':
                    data += '<li><a href = ' + uri + each + '>' + each + '</a></li>'
                else:
                    data += '<li><a href = ' + uri + '/' + each + '>' + each + '</a></li>'
            return 200, 'text/html', len(data), data.encode()
        elif os.path.isfile(p):
            p = open(p, 'rb')
            data = p.read()
            p.close()
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