# ------------------------- #
# Assignment 1              #
# Matthew Goldsberry        #
# ------------------------- #

# import necessary libraries
from socket import *
import threading
import signal
import sys

# global variable to hold the server socket (Needed for SIGINT handling)
serverSocket = None
shutdown_flag = False

class HttpRequest(threading.Thread):\
    # define the carriage return line feed for HTTP
    CRLF = "\r\n"

    # Constructor
    def __init__(self, socket):
        # initialize the thread
        super().__init__()
        # assign the client socket
        self.socket = socket
        self.daemon = True

    # run method for handlign the request in a seperate thread
    def run(self):
        try:
            # process the HTTP request
            self.processRequest()
        except Exception as e:
            # if any execptions occur, print them
            print(e)

    # method to process the incoming HTTP request
    def processRequest(self):
        # get a reference to the socket's input and output streams
        inputStream = self.socket.makefile('r')
        outputStream = self.socket.makefile('wb')

        # set up input stream filters
        bufferedReader = inputStream

        # get the request line of the HTTP request message
        requestLine = bufferedReader.readline().strip()

        # display header for the request message
        print("\nREQUEST:")
        print("--------------------------------------\n")

        # display the request line
        print("\n" + requestLine)

        # get the filename from the request line
        filename = self.get_filename(requestLine)

        # open the file, returns file and a flag for if it was successfully opened or not
        file, fileExists = self.open_file(filename)

        # generate the response
        statusLine, contentTypeLine, entityBody = self.create_response_message(filename, fileExists)

        # get and display the header lines
        while (headerLine := bufferedReader.readline().strip()):
            print(headerLine)

        print("\n")

        # close streams and sockets
        outputStream.close()
        bufferedReader.close()
        self.socket.close()

    def get_filename(self, requestLine):
        # split the request line by spaces
        tokens = requestLine.split()

        # grab the filename which will be in index 1 of a request line
        filename = tokens[1]

        # prepend a dot to the filename to specify starting in the current directory
        filename = "." + filename

        return filename
    
    def content_type(self, filename):
        # skip the first "." in filename and split by ".", the second item will be the filetype
        _, filetype = filename[1:].split(".")

        # Check if the filetype is equal to any of the filetypes used in this lab
        if filetype == "html":
            # return the content type for html
            return "text/html"
        elif filetype == "jpg":
            # return the content type for jpg
            return "image/jpg"
        else:
            assert "Not one of the specified file types"

    def open_file(self, filename):
        # initialize local variables
        file = None
        fileExists = True

        # try to open the file
        try: 
            # open the file in read mode
            file = open(filename, 'rb')
        except FileNotFoundError:
            # if the file is not found set the flag to false
            fileExists = False
        
        # return the file and flag of if it was successfully opened 
        return file, fileExists
        
    def create_response_message(self, filename, fileExists):
        # initialize local variables
        statusLine = None
        contentTypeLine = None
        entityBody = None 
        CRLF="\r\n"

        if (fileExists):
            statusLine = "HTTP/1.1 200 OK" + CRLF
            contentTypeLine = "Content-type: " + self.content_type(filename) + CRLF
        else: 
            statusLine = "HTTP/1.1 404 Not Found" + CRLF
            contentTypeLine = "Content-type: text/html" + CRLF
            entityBody = "<HTML>" + "<HEAD><TITLE>Not Found</TITLE><HEAD>" + "<BODY>Not Found</BODY>" + "</HTML>"
        
        # print generated response
        print("\nRESPONSE:")
        print("--------------------------------------\n")
        print(statusLine)
        print(contentTypeLine)
        if not fileExists: print(entityBody)

        # return the created lines to the response message
        return statusLine, contentTypeLine, entityBody



# Signal handler to shut down the server when SIGINT is sent (Ctrl + C)
def signal_handler(sig, frame):
    print("\nServer is shutting down...")
    shutdown_flag = True
    # if the server socket is open, close it
    if serverSocket:
        serverSocket.close()
    print("Server Shutdown.")
    # exit the program
    exit(0)


# main function to run the web server
def webserver():
    # set the port number 
    port = 6789

    # establish the listen socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('',port))
    serverSocket.listen(1)
    print(f"Server is running on port {port}...")

    # set a timeout time to allow for breaks for SIGINT to be read (Ctrl + C)
    serverSocket.settimeout(3)

    # register signal handler for SIGINT (Ctrl + C)
    signal.signal(signal.SIGINT, signal_handler)

    # process HTTP service requests in an infinite loop.
    while not shutdown_flag:
        try:
            print("Waiting for a connection...")

            # listen for a TCP connection request.
            connectionSocket, addr = serverSocket.accept()
            # print(f"Connection from {addr} has been established.")

            # construct an object to process the HTTP request message
            request = HttpRequest(connectionSocket)

            # start the thread
            request.start()
        # ignore the TimeoutErrors from the settimeout
        except TimeoutError:
            continue
        # Handle the case when the server socket is closed
        except OSError as e:
            if shutdown_flag:
                break

if __name__ == "__main__":
    webserver()