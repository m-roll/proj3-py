from routerlib.message import MessageEncoder
import socket
import json


class Neighbor():

    def __init__(self, my_router_addr, network_addr, type):
        self.my_router_addr = my_router_addr
        self.network_addr = network_addr
        self.type = type
        self.socket = socket.socket(
            socket.AF_UNIX, socket.SOCK_SEQPACKET)
        self.socket.setblocking(0)
        self.socket.connect(network_addr)

    def get_socket(self):
        return (self.network_addr, self.socket)

    def get_addr(self):
        return self.network_addr

    def transmit(self, msg):
        str = json.dumps(msg, cls=MessageEncoder).encode()
        print('transmitting:')
        print(str)
        self.socket.send(str)
