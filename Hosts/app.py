from socket import socket, AF_INET, SOCK_DGRAM

class App:
    server_sockets = {int : socket} # {dstport : socket}

    def __init__(self: str, ip: str, dstports: list[str]):
        self.ip = ip
        self.dstports = dstports
        for port in dstports:
            self.server_sockets[port] = socket(AF_INET, SOCK_DGRAM)
            self.server_sockets[port].bind(ip, port)
