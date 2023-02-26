# CS 656 Assignment 1

This is a program that complete both TCP and UDP socket programming in a client server environment.
* Programming Language: Python 3.9
* IDE: Pycharm

## How to run the program
Command line for server:
```commandline
./server.sh <req_code> <file_to_send>
```
- <req_code>: an integer for authentication
- <file_to_send>: a string for the name of file to be sent
Command line for client:
```commandline
./client.sh <server_address> <n_port> <mode> <req_code> <file_received>
```
- server_address: a string of server IP address or hostnames
- n_port: an integer of port number of server
- mode: can either be 'P ' or 'A indicating whether the client should run in Passive or Active mode
- req_code: an integer for authentication
- file_received: a string for the name of the received file

If permission denied when run the server.sh or client.sh scripts, run the following command first:
```commandline
chmod +x server.sh 
chmod +x client.sh
```
