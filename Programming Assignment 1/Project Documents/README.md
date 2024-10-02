**WebServer.py**

This still needs to be tested for successful completion of task 1.

**FTPCLient.py**

At the bottom of the file there is a commented out section of code that is the main.
If you run that code it will place a copy of the ftp_text.txt in the root directory of this repository (computernetworks-fall2024)
Before Running
- Make sure the Docker container is running 
- you can check that it is properly running ftp by running `docker ps` then `docker logs <ID>` and then `Running vsftpd` should be present
- Also make sure that a connection is made on FileZilla to `localhost` with the username and password enter and the port set to `21`

**What is left?**

Need to implment FTPClient into Webserver 