**How to Start up FTP**
- make sure IPv6 is disabled (Control Panel->Network->The Wift->Propteries->uncheck IPv6)
- disable firewalls(Control Panel->System and Security->Firewalls->Turn on/off->select off for both)
- Open Docker
- In a terminal run the following
    - `docker run --rm -it -p 20:20 -p 21:21 -p 4559-4564:4559-4564 -e FTP_USER=<USER_NAME> -e FTP_PASSWORD=<PASSWORD> docker.io/panubo/vsftpd:latest`
    - `docker container ls`
    - `docker exec -it <CONTAINER_ID> /bin/bash`
    - `chown ftp:ftp /srv`


**WebServer.py**

Tested and successful... now adding the last bit connecting to the FTP

Notes for testing. Run from the Programming Assignment 1 directory with the following command:
    `python webserver/WebServer.py`

**FTPCLient.py**

At the bottom of the file there is a commented out section of code that is the main.
If you run that code it will place a copy of the ftp_text.txt in the root directory of this repository (computernetworks-fall2024)
Before Running
- Make sure the Docker container is running 
- you can check that it is properly running ftp by running `docker ps` then `docker logs <ID>` and then `Running vsftpd` should be present
- Also make sure that a connection is made on FileZilla to `localhost` with the username and password enter and the port set to `21`

**What is left?**

Look at clean up and comments

I need to talk to prof
- After letting the server run for a little i will get a requestLine of ""...
- Is that exepcted...
- Why is that???
- Is the way I addressed it fine