import socket
import re
import os

# based on FtpClient.java template provided

class FtpClient:
    
    def __init(self):
        """Constructor"""
        self.CRLF = "\r\n"
        self.DEBUG = True # Debug Flag
        self.controlSocket = None
        self.controlReader = None
        self.controlWriter = None
        self.currentResponse = ""

    def connect(sef, username, password):
        """
        Connect to the FTP server
        @param username: the username you use to login to your FTP session
        @param password: the password associated with the username
        """
        pass

    def getFile(self, file_name):
        """
        Retrieve the file from FTP server after connection is established
        @param file_name: the name of the file to retrieve
        """
        pass

    def disconnect(self):
        """Close the FTP connection"""
        try:
            self.controlReader.close()
            self.controlWriter.close()
            self.controlSocket.close()
        except IOError as e:
            print(f"IOExceptionL {e}")

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
            response = self.controlReader.readline().strip()
            if self.DEBUG:
                print(f"Current FTP response: {response}")
            if not response.startswith(str(expected_response_code)):
                raise IOError(f"Bad response: {response}")
        except IOError as e:
            print(f"IOException: {e}")
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
                print(f"Current FTP response: {self.current_response}")
            if not self.currentResponse.startswith(str(expected_code)):
                response_status = False
                raise IOError(f"Bad response: {self.currentResponse}")
        except IOError as e:
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
        pattern = re.compile(r"((.*?)\)")
        matcher = pattern.search(response_line)
        if matcher:
            str_parts = matcher.group(1).split(",")
            if self.DEBUG:
                print(f"Port integers: {str_parts[4]},{str_parts[5]}")
            data_port = int(str_parts[4]) * 256 + int(str_parts[5])
            if self.DEBUG:
                print(f"Data Port: {data_port}")
        return data_port
    
    def createLocalFile(dis, file_name):
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