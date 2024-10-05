import socket
import re
import os

# based on FtpClient.java template provided

class FtpClient:
    
    def __init__(self):
        """Constructor"""
        self.CRLF = "\r\n"
        self.DEBUG = False # Debug Flag
        self.controlSocket = None
        self.controlReader = None
        self.controlWriter = None
        self.currentResponse = ""

    def connect(self, username, password):
        """
        Connect to the FTP server
        @param username: the username you use to login to your FTP session
        @param password: the password associated with the username
        """
        try:
            # establish the control socket
            self.controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.controlSocket.connect(('localhost', 21))

            # get references to the socket input and output streams
            self.controlReader = self.controlSocket.makefile('rb')
            self.controlWriter = self.controlSocket.makefile('wb')


            # check if the initial connection response code is OK
            if self.checkResponse(220):
                if self.DEBUG:
                    print("\nSuccessfully connected to FTP server")
            
            # send username and password to ftp server
            self.sendCommand(f"USER {username}\r\n", 331)
            self.sendCommand(f"PASS {password}\r\n", 230)

        except socket.gaierror as e: # Python's version of UnknownHostException
            print(f"UnknownHostException: {e}")
        except IOError as e:
            print(f"IOException: {e}")

    def getFile(self, file_name):
        """
        Retrieve the file from FTP server after connection is established
        @param file_name: the name of the file to retrieve
        """
        data_port = 0
        try:
            # change to current (root) directory first
            self.sendCommand("CWD /\r\n", 250)

            # set to passive mode and retrieve the data port number from response
            self.currentResponse = self.sendCommand("PASV\r\n", 227)
            data_port = self.extractDataPort(self.currentResponse)

            # connect to the data port
            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.connect(('localhost',data_port))
            data_reader = data_socket.makefile('rb')

            # download file from ftp server
            if not self.sendCommand(f"RETR {file_name}\r\n", 150):
                # if it returns None, inidicating file not found, end function
                return

            # check if the transfer was successful
            if self.checkResponse(226):
                if self.DEBUG:
                    print("getFile successful")
            else:
                if self.DEBUG:
                    print("getFile unsuccessful")

            # write data on a local file
            self.createLocalFile(data_reader, file_name)

        except socket.gaierror as e:
            print(f"UnknownHostException: {e}")
        except IOError as e:
            print(f"IOException: {e}")

    def disconnect(self):
        """Close the FTP connection"""
        try:
            self.controlReader.close()
            self.controlWriter.close()
            self.controlSocket.close()
        except IOError as e:
            print(f"IOException: {e}")

    def sendCommand(self, command, expected_response_code):
        """
        Send ftp command 
        @param command: the full command line to send to the ftp server
        @param expected_code: the expected response code from the ftp server
        @return the response line from the ftp server after sending the command
        """
        response = ""
        try:
            self.controlWriter.write(command.encode())
            self.controlWriter.flush()
            response = self.controlReader.readline()
            if self.DEBUG:
                print(f"Current FTP response: {response}")
            if not response.startswith(str(expected_response_code).encode()):
                raise IOError(f"Bad response: {response}")
        except IOError as e:
            if self.DEBUG:
                print(f"IOException: {e}")
            response = None
        return response

    def checkResponse(self, expected_code):
        """
        Check the validity of the ftp response, the response code should
        correspond to the expected response code
        @param expected_code: the expected ftp response code
        @return response status: true if successful code
        """
        response_status = True
        try:
            self.currentResponse = self.controlReader.readline()
            if self.DEBUG:
                print(f"Current FTP response: {self.currentResponse}")
            if not self.currentResponse.startswith(str(expected_code).encode()):
                response_status = False
                raise IOError(f"Bad response: {self.currentResponse}")
        except IOError as e:
            if self.DEBUG:
                print(f"IOException: {e}")
        return response_status

    def extractDataPort(self, response_line):
        """
        Given the complete ftp response line of setting data transmission mode
        to passive, extract the port to be used for data transfer
        @param response_line: the ftp response line
        @return the data port number 
        """
        data_port = 0
        pattern = re.compile(r"\((.*?)\)")
        matcher = pattern.search(response_line.decode())
        if matcher:
            str_parts = matcher.group(1).split(",")
            if self.DEBUG:
                print(f"Port integers: {str_parts[4]},{str_parts[5]}")
            data_port = int(str_parts[4]) * 256 + int(str_parts[5])
            if self.DEBUG:
                print(f"Data Port: {data_port}")
        return data_port
    
    def createLocalFile(self, dis, file_name):
        """
        Create the file locally after retreiving data over the FTP data stream.
        @param dis: the data input stream 
        @param file_name: the name of the file to create 
        """
        buffer = 1024
        try:
            fos = open(file_name, 'wb')
            while bytes := dis.read(buffer):
                fos.write(bytes)
            dis.close()
            fos.close()
        except FileNotFoundError as e:
            print(f"FileNotFoundError: {e}")
        except IOError as e:
            print(f"IOError: {e}")

# VERIFICATION FOR IT WORKING
# if __name__ == "__main__":
#     ftp = FtpClient()
#     ftp.connect("matt", "123")
#     ftp.getFile("ftp_test.txt")