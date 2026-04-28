import socket

def is_valid_host(host):
    try:
        socket.gethostbyname(host)
        return True
    except socket.error:
        return False