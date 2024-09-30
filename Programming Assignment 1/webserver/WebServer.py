# ------------------------- #
# Assignment 1              #
# Matthew Goldsberry        #
# ------------------------- #

from socket import *
import threading

class HttpRequest(threading.Thread):
    CRLF = "\r\n"

    # Constructor
    def __init__(self, socket):
        super().__init__()
        self.socket = socket

    def run(self):
        try:
            self.processRequest()
        except Exception as e:
            print(e)

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

        # close streams and sockets
        outputStream.close()
        bufferedReader.close()
        self.socket.close()


def webserver():
    # set the port number 
    port = 6789

    # establish the listen socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('',port))
    serverSocket.listen(1)
    print(f"Server is running on port {port}...")

    try:
        # process HTTP service requests in an infinite loop.
        while True:
            print("Waiting for a connection...")

            # listen for a TCP connection request.
            connectionSocket, addr = serverSocket.accept()
            print(f"Connection from {addr} has been established.")

            # construct an object to process the HTTP request message
            request = HttpRequest(connectionSocket)
            # start the thread
            request.start()
    except KeyboardInterrupt:
        # Handle the SIGINT signal (ctrl + c)
        print("Server is shutting down...")
        serverSocket.close()

if __name__ == "__main__":
    webserver()