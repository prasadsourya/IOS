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
'''

import socket
import os
import mimetypes
import sys
import time
import signal
import multiprocessing
class HTTPServer:

    def funct(self):
        while True:
            conn, addr = self.s.accept()
            with conn:
                #print("Connected by", addr)
                # TODO read the request and extract the URI 
                r = conn.recv(1024)
                # print(r)
                r = str(r)
                if r != "b''":
                    spt = r.split(' ')
                    #print(spt)
                    #spt = spt[1].split('/')
                    filename = spt[1]
                #print(filename)
                # TODO update the parameter with the request URI
                uri = ""
                uri = filename
                if uri != "/favicon.ico":
                    code, c_type, c_length, data = self.get_data(uri)
                    response = self.response_headers(code, c_type, c_length).encode() + data
                    conn.sendall(response)
                    conn.close()

    def __init__(self, IP, port):
        super().__init__()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as self.s:
            self.s.bind((IP, port))
            self.s.listen()
            print("Socket is listening")
            for _  in range(8):
                process = multiprocessing.Process(target=self.funct, args=())
                process.start()
            
    
    def get_data(self, uri):
        '''
            TODO: This function has to be updated for M2
        '''
        #print("uri : "+uri)
        sample = uri.split("/")
        if (sample[1] == "bin") :
            #print("Is this working")
            flag = True
            location = os.getcwd()+"/tws-bin/"+sample[2]
            if '.' in sample[2]:
                flag = False
            stdin  = sys.stdin.fileno()
            stdout = sys.stdout.fileno()
            parentStdin, childStdout  = os.pipe() 
            # childStdin,  parentStdout = os.pipe() 
            pid = os.fork()
            if pid == 0:
                os.close(parentStdin)
                # os.close(parentStdout)
                # os.dup2(childStdin, stdin)
                os.dup2(childStdout, stdout)
                if flag:
                    os.execv(location, sys.argv)
                else:
                    exec(open(location).read())                    
                sys.stdout.flush()
                return
            else :
                # os.close(childStdin)
                os.close(childStdout)
                os.dup2(parentStdin,  stdin)
                # os.dup2(parentStdout, stdout)
                if flag:
                    data = ""
                    while True:
                        try:
                            data += "<h3>"+input()+"</h3>"
                        except EOFError:
                            break
                    return 200, "text/html", len(data), data.encode()
                else:
                    counter = 0
                    while True:
                        counter += 1
                        var = os.waitpid(pid, os.WNOHANG)
                        if (os.WEXITSTATUS(var[1])):
                            stdin = os.fdopen(parentStdin)
                            data = stdin.read()
                            return 200, "text/html", len(data), data.encode()
                        elif counter == 10:
                            os.kill(pid, signal.SIGSTOP)
                            data = "<h3>Terminated due to Timeout</h3>"
                            return 200, "text/html", len(data), data.encode()
                        time.sleep(1)
                
        if uri == "/":
            data = ""
            data += "<body>\n<h2>Directory listing for "+"www/"+"</h2>\n"
            loc = os.getcwd()+"/www/"
            list = os.listdir(loc)
            for i in list:
                data += "<li><a href="+"/www/"+i+">"+i+"</a></li>"
            return 200, "text/html", len(data), data.encode()
        location = os.getcwd()
        location += uri
        boolean = os.path.isfile(location)
        if os.path.isdir(location):
            list = os.listdir(location)
            s = ""
            s += "<body>\n<h2>Directory listing for "+uri+"</h2>\n"
            for i in list:
                s += "<li><a href="+uri+"/"+i+">"+i+"</a></li>"
            return 200, "text/html", len(s), s.encode()
        elif boolean:
            fileread = open(location, "rb")
            data = fileread.read()
            type = mimetypes.MimeTypes().guess_type(location)[0]
            return 200, type, len(data), data
        else:
            data = "<h1>File Not Found</h1>"        
            return 404, "text/html", len(data), data.encode()
    
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
    HTTPServer('127.0.0.1', 8889)

if __name__ == "__main__":
    main()                   