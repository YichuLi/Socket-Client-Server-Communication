from socket import *
import sys


def get_r_port():
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 0))  # system will pick a port number that is not occupied
    r_port = s.getsockname()[1]
    s.close()
    return r_port


def checker():
    if len(sys.argv) != 3:
        print('Usage: \'python server.py <req_code> <file_to_send>\'')
        sys.exit(1)
    try:
        int(sys.argv[1])
    except ValueError:
        print("req_code must be an integer.")
        sys.exit(1)


def udp_socket(s_port):
    server_sock = socket(AF_INET, SOCK_DGRAM)
    try:
        server_sock.bind(('', s_port))
    except error as e:
        server_sock.bind(('', 0))
        s_port = server_sock.getsockname()[1]
    server_sock.close()
    print("SERVER_PORT=" + str(s_port))
    return s_port


checker()  # check for argv format
sever_port = 5001
req_code = sys.argv[1]
file_name = sys.argv[2]
n_port = udp_socket(sever_port)  # get the n_port
udp_sock = socket(AF_INET, SOCK_DGRAM)
udp_sock.bind(('', n_port))

while True:
    message, clientAddress = udp_sock.recvfrom(2048)
    msg_arr = message.split()
    print(str(msg_arr))
    if len(msg_arr) != 3:
        print("client's sending format is wrong")
        sys.exit(1)
    if msg_arr[0].decode() == "PORT":  # Active mode
        if msg_arr[2].decode() != req_code:  # wrong req_code
            print("deny for transfer")
            udp_sock.sendto("0".encode(), clientAddress)
        else:
            print("ok for transfer")
            udp_sock.sendto("1".encode(), clientAddress)
            tcp_sock = socket(AF_INET, SOCK_STREAM)
            # tcp_port = get_r_port()
            # tcp_sock.bind('', tcp_port)
            # tcp_sock.listen(1)
            tcp_sock.connect((clientAddress[0], int(msg_arr[1].decode())))
            with open(file_name, 'rb') as f:
                data = f.read(1024)
                while data:
                    tcp_sock.sendall(data)
                    data = f.read(1024)
            tcp_sock.close()
    else:
        print("exception")
