
from routerlib.neighbor import Neighbor
import select
import json
from routerlib.message import Message


class RouterPorts():

    def __init__(self, relationships, msg_callback):
        self.ports = {}
        self.msg_callback = msg_callback
        for relationship in relationships:
            network, relation = relationship.split("-")
            my_ip = self._get_rel_ip(network)
            port = Neighbor(my_ip, network, relation)
            self.ports[network] = port

    def _get_rel_ip(self, network):
        addr_split = network.split(".")
        addr_split = addr_split[:-1]
        addr_split.append("1")
        return ".".join(addr_split)

    def get_sockets(self):
        ports = self.ports.values()
        return list(map(lambda port: port.get_socket(), ports))

    def get_ports(self):
        return self.ports

    def run(self):
        """ main loop for the router """
        while True:
            sock_tuples = self.get_sockets()
            sock_map = {}
            for addr, sock in sock_tuples:
                sock_map[addr] = sock
            socks = select.select(sock_map.values(), [], [], 0.1)[0]
            for conn in socks:
                try:
                    k = conn.recv(65535)
                except:
                    # either died on a connection reset, or was SIGTERM's by parent
                    print("connection dead?")
                    return
                if k:
                    for addr in sock_map:
                        if sock_map[addr] == conn:
                            src_neighbor = self.ports[addr]
                    parsed = json.loads(k)
                    msg_type = parsed['type']
                    msg_source = parsed['src']
                    msg_dest = parsed['dst']
                    msg_ctnt = parsed['msg']
                    msg = Message(msg_type, msg_source, msg_dest, msg_ctnt)
                    self.msg_callback(src_neighbor, msg)
                else:
                    return
