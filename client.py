from socket import *
import sys
import ipaddress


# get an available port number if necessary
def get_r_port():
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 0))  # system will pick a port number that is not occupied
    ava_port = s.getsockname()[1]
    s.close()
    return ava_port


# check the format of argv command
def checker():
    try:
        ipaddress.ip_address(server_address)
    except ValueError:
        print('address/netmask is invalid: %s' % server_address)
        sys.exit(1)
    try:
        int(n_port)
    except ValueError:
        print("n_port must be an integer.")
        sys.exit(1)
    if int(n_port) < 1024 or int(n_port) > 65535:
        print("n_port must be between [1024, 65535].")
        sys.exit(1)
    if mode != 'P' and mode != 'A':
        print("mode should be either 'P' or 'A'.")
        sys.exit(1)
    try:
        int(req_code)
    except ValueError:
        print("req_code must be an integer.")
        sys.exit(1)


def handle(ip, port, m, req):
    udp_sock = socket(AF_INET, SOCK_DGRAM)
    if m == 'A':  # Active mode
        r_port = get_r_port()
        message = "PORT " + str(r_port) + " " + str(req)
        tcp_sock = socket(AF_INET, SOCK_STREAM)
        tcp_sock.bind(('', r_port))
        tcp_sock.listen(1)
        udp_sock.sendto(message.encode(), (ip, int(port)))
        acknowledgement, s_address = udp_sock.recvfrom(2048)
        ack = int(acknowledgement.decode())
        if ack == 0:
            sys.exit()  # wrong req_code leads to system exiting gracefully
        elif ack == 1:
            connection_socket, addr = tcp_sock.accept()
            with open(file_received, 'wb') as f:
                while True:
                    data = connection_socket.recv(1024)
                    if not data:
                        break
                    f.write(data)
    elif m == 'P':  # Passive mode
        message = "PASV " + str(req)
        udp_sock.sendto(message.encode(), (ip, int(port)))
        acknowledgement, s_address = udp_sock.recvfrom(2048)
        r_port = int(acknowledgement.decode())
        if r_port == 0:
            sys.exit(1)  # wrong req_code leads to system exiting gracefully
        else:
            tcp_sock = socket(AF_INET, SOCK_STREAM)
            tcp_sock.connect((ip, r_port))  # init the connection with server
            with open(file_received, 'wb') as f:
                while True:
                    data = tcp_sock.recv(1024)
                    if not data:
                        break
                    f.write(data)
    else:
        print("exception")
        sys.exit(1)


if len(sys.argv) != 6:
    print('Usage: \'python client.py <server address> <n_port> <mode> <req_code> <file_received>\'')
    sys.exit(1)
server_address = sys.argv[1]
if server_address == 'localhost':
    server_address = '127.0.0.1'
n_port = sys.argv[2]
mode = sys.argv[3]
req_code = sys.argv[4]
file_received = sys.argv[5]
checker()
handle(server_address, n_port, mode, req_code)
