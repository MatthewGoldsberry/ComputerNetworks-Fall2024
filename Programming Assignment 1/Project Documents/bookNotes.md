# Client-Server Application using UDP

![Image description](https://cite-media.pearson.com/legacy_paths/1641fede-4780-43e4-8e24-4bb30fac1cb7/Fig02-027.png)

**UDP CLIENT**

Book Provided Code:
```
from socket import *
serverName = 'hostname'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Input lowercase sentence:')
clientSocket.sendto(message.encode(),(serverName,ServerPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
```

**UDP SERVER**

Book Provided Code:
```
from socket import *
serverName = 'hostname'
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
```


# Client-Server Application using TCP

![Image description](https://cite-media.pearson.com/legacy_paths/15e767b2-c559-42ba-9dc6-4d760c59b747/Fig02-028.png)

![Image description](https://cite-media.pearson.com/legacy_paths/46eb9d3b-3ef4-42a8-811c-fda552301dd2/Fig02-029.png)

**TCP CLIENT**

Book Provided Code:
```
from socket import *
serverName = 'servername'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.connect((serverName,serverPort))
sentence = input('Input lowercase sentence:')
clientSocket.send(message.encode())
modifiedMessage = clientSocket.recvfrom(1024)
print(modifiedMessage.decode())
clientSocket.close()
```

**TCP SERVER**

Book Provided Code:
```
from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to recieve')
while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    captializedSentence = sentence.upper()
    connetionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()
```