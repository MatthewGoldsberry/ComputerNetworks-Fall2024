# ------------------------- #
# Assignment 1              #
# Matthew Goldsberry        #
# ------------------------- #

# import necessary libraries
from socket import *
import threading
import signal
from FTPClient import FtpClient

# global variable to hold the server socket (Needed for SIGINT handling)
serverSocket = None
shutdown_flag = False

class HttpRequest(threading.Thread):\

    def __init__(self, socket):
        """Constructor"""
        # initialize the thread
        super().__init__()
        # assign the client socket
        self.socket = socket
        self.daemon = True
        # define the carriage return line feed for HTTP
        self.CRLF = "\r\n"
        # holds the file
        self.file = None

    def run(self):
        """Handle the HTTP request in a seperate thread"""
        try:
            # process the HTTP request
            self.processRequest()
        except Exception as e:
            # if any execptions occur, print them
            print(e)

    def processRequest(self):
        """Process the incoming HTTP request"""
        # get a reference to the socket's input and output streams
        inputStream = self.socket.makefile('rb')
        outputStream = self.socket.makefile('wb')

        # set up input stream filters
        bufferedReader = inputStream

        # get the request line of the HTTP request message
        requestLine = bufferedReader.readline().strip()

        # Check if requestLine is None or empty
        if not requestLine:
            # Exit the function
            return

        # display header for the request message
        print("\nREQUEST:")
        print("--------------------------------------")

        # display the request line
        print("\n" + requestLine.decode())

        # get and display the header lines
        self.display_header_lines(bufferedReader)

        # get the filename from the request line
        filename = self.get_filename(requestLine.decode())

        # open the file, returns file and a flag for if it was successfully opened or not
        self.file, fileExists = self.open_file(filename)

        # generate the response
        statusLine, contentTypeLine, entityBody = self.create_response_message(filename, fileExists)

        # write the response into the output stream for the client
        self.write_header_for_client(outputStream, statusLine, contentTypeLine)

        # send the message 
        self.send_response_to_client(self.file, filename, fileExists, outputStream, entityBody)

        # close streams and sockets
        outputStream.close()
        bufferedReader.close()
        self.socket.close()

    def display_header_lines(self, bufferedReader):
        """Read in from bufferedReader and display the remaining headerlines"""
        while (headerLine := bufferedReader.readline().strip()):
            print(headerLine.decode())

    def get_filename(self, requestLine):
        """Grab the filename from the request line"""
        # split the request line by spaces
        tokens = requestLine.split()

        # grab the filename which will be in index 1 of a request line
        filename = tokens[1]

        # prepend a dot to the filename to specify starting in the current directory
        filename = "." + filename

        return filename
    
    def open_file(self, filename):
        """Try to open the specified file and return the file object and flag for if the file exists"""
        # initialize local variables
        fileExists = True

        # try to open the file
        try: 
            # open the file in read mode
            self.file = open(filename, 'rb')
        except FileNotFoundError:
            # if the file is not found set the flag to false
            fileExists = False
        
        # return the file and flag of if it was successfully opened 
        return self.file, fileExists

    def content_type(self, filename):
        """Helper function for create_response_message. Converts filename to MIME type"""
        # Check if the filename endswith is true for any of the filetypes used in this lab
        if filename.endswith(".htm") or filename.endswith(".html"):
            # return the MIME type for html
            return "text/html"
        elif filename.endswith(".jpg"):
            # return the MIME type for jpg
            return "image/jpg"
        elif filename.endswith(".gif"):
            # return the MIME type for gif
            return "image/gif"
        elif filename.endswith(".txt"):
            # return the MIME type for txt
            return "text/plain"
        else:
            # return generatic placeholder for binary data
            return "application/octet-stream"
        
    def print_response(self, statusLine, contentTypeLine, entityBody):
        """Helper function for create_response_message. Displays the generated response"""
        print("\nRESPONSE:")
        print("--------------------------------------")
        print(statusLine)
        print(contentTypeLine)
        if entityBody: print(entityBody)
        
    def create_response_message(self, filename, fileExists):
        """Contrust the HTTP response message"""
        # if the file exists do not create a entityBody
        if fileExists:
            # generate 200 status line, specify content_type (in MIME) of the file and entityBody is None
            statusLine = "HTTP/1.1 200 OK" + self.CRLF
            contentTypeLine = "Content-type: " + self.content_type(filename) + self.CRLF
            entityBody = None 
        else: 
            if (self.content_type(filename) != "text/plain"):
                # generate 404 status line (since file was not found), specify the content type of the error
                # message (in MIME) which is text/html, and set entityBody to a basic error message in HTML
                statusLine = "HTTP/1.1 404 Not Found" + self.CRLF
                contentTypeLine = "Content-type: text/html" + self.CRLF
                entityBody = "<HTML>" + "<HEAD><TITLE>Not Found</TITLE><HEAD>" + "<BODY>Not Found</BODY>" + "</HTML>"
            else:
                statusLine = "HTTP/1.1 200 OK" + self.CRLF
                contentTypeLine = "Content-type: text/plain" + self.CRLF

                # create an instance of ftp client
                ftpClient = FtpClient()

                # connect to the ftp server
                ftpClient.connect("matt", "123")

                # retrieve the file from the ftp server
                ftpClient.getFile(filename)

                # disconnect from ftp server
                ftpClient.disconnect()

                # assign input stream to read the recently the recently ftp-downloaded file
                try:
                    self.file = open(filename, 'rb')
                except:
                    # if the open fails, it means getFile did not find a file and thus could 
                    # not make a local version. So display Not Found message
                    statusLine = "HTTP/1.1 404 Not Found" + self.CRLF
                    contentTypeLine = "Content-type: text/html" + self.CRLF
                    entityBody = "<HTML>" + "<HEAD><TITLE>Not Found</TITLE><HEAD>" + "<BODY>Not Found</BODY>" + "</HTML>"

        # print generated response
        self.print_response(statusLine, contentTypeLine, entityBody)

        # return the created lines to the response message
        return statusLine, contentTypeLine, entityBody

    def write_header_for_client(self, outputStream, statusLine, contentTypeLine):
        """Writes the headers for the output stream"""
        # send the status line 
        outputStream.write(statusLine.encode())

        # send the content type line
        outputStream.write(contentTypeLine.encode())

        # send end-of-header line 
        outputStream.write(self.CRLF.encode())

    def send_bytes(self, file, outputStream):
        """Send the file content to the output stream in chunks"""
        # 1k bufer to hold bytes on their way to the socket
        buffer = 1024

        # copy requested file into the socket's output stream
        while bytes := file.read(buffer):
            outputStream.write(bytes)

    def send_response_to_client(self, file, filename, fileExists, outputStream, entityBody):
        """Send the entity body to output stream"""
        # if the file exists send the bytes from the file to outputStream in chunks and close file
        if (fileExists):
            self.send_bytes(file, outputStream)
            file.close()
        else:
            if (self.content_type(filename) != "text/plain" or entityBody != None):
                outputStream.write(entityBody.encode())
            else:
                self.send_bytes(file, outputStream)


def signal_handler(sig, frame):
    """Signal handler to shut down the server when SIGINT is sent (Ctrl + C)"""
    print("\nServer is shutting down...")
    shutdown_flag = True
    # if the server socket is open, close it
    if serverSocket:
        serverSocket.close()
    print("Server Shutdown.")
    # exit the program
    exit(0)


def webserver():
    """Main function to run the web server"""
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

    print("Waiting for a connection...")

    # process HTTP service requests in an infinite loop.
    while not shutdown_flag:
        try:
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