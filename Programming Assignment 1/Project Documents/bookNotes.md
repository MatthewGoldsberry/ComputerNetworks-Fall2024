# Client-Server Application using UDP

![Image description](https://cite-media.pearson.com/legacy_paths/1641fede-4780-43e4-8e24-4bb30fac1cb7/Fig02-027.png)

Book Provided Code:
```
from socket import *
serverName = 'hostname'
serverPort = 12000
clientSocket = socker(AF_INET, SOCK_DGRAM)
message = input('Input lowercase sentence:')
clientSocket.sendto(message.encode(),(serverName,ServerPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
```