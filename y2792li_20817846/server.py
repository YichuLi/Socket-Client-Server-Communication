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
        print('Usage: python server.py <req_code> <file_to_send>')
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
    except error:
        server_sock.bind(('', 0))
        s_port = server_sock.getsockname()[1]
    server_sock.close()
    print("SERVER_PORT=" + str(s_port))
    return s_port


def handle(req_code, file_name, n_port):
    udp_sock = socket(AF_INET, SOCK_DGRAM)
    udp_sock.bind(('', n_port))

    while True:
        message, client_address = udp_sock.recvfrom(2048)
        msg_arr = message.split()

        if msg_arr[0].decode() == "PORT":  # Active mode
            if len(msg_arr) != 3:
                print("client's sending format is incorrect")
                sys.exit(1)
            if msg_arr[2].decode() != req_code:  # wrong req_code
                udp_sock.sendto("0".encode(), client_address)
            else:
                udp_sock.sendto("1".encode(), client_address)
                tcp_sock = socket(AF_INET, SOCK_STREAM)
                tcp_sock.connect((client_address[0], int(msg_arr[1].decode())))  # server init connection on r_port
                try:
                    with open(file_name, 'rb') as f:
                        file_data = f.read(1024)  # 1024 bytes is sufficient for this system
                except FileNotFoundError:
                    exit(1)
                try:
                    tcp_sock.sendall(file_data)
                except error:
                    exit(1)
                tcp_sock.close()

        elif msg_arr[0].decode() == "PASV":  # Active mode
            if len(msg_arr) != 2:
                print("client's sending format is incorrect")
                sys.exit(1)
            if msg_arr[1].decode() != req_code:  # wrong req_code
                udp_sock.sendto("0".encode(), client_address)
            else:
                tcp_port = get_r_port()
                tcp_sock = socket(AF_INET, SOCK_STREAM)
                tcp_sock.bind(('', tcp_port))
                tcp_sock.listen(1)
                udp_sock.sendto(str(tcp_port).encode(), client_address)
                conn_sock, addr = tcp_sock.accept()
                try:
                    with open(file_name, 'rb') as f:
                        file_data = f.read(1024)
                except FileNotFoundError:
                    exit(1)
                try:
                    conn_sock.sendall(file_data)
                except error:
                    exit(1)
                conn_sock.close()


checker()  # check for argv format
sever_port = 5001
r_code = sys.argv[1]
f_name = sys.argv[2]
port = udp_socket(sever_port)  # get the n_port
handle(r_code, f_name, port)
