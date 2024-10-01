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

        # display the request line
        print("\n" + requestLine)

        # get and display the header lines
        while (headerLine := bufferedReader.readline().strip()):
            print(headerLine)

        print("\n")

        # close streams and sockets
        outputStream.close()
        bufferedReader.close()
        self.socket.close()


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