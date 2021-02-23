
from routerlib.neighbor import Neighbor


class RouterPorts():

    def __init__(self, relationships):
        self.ports = {}
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
        return list(map(lambda port: port.get_socket()[1], ports))

    def get_ports(self):
        return self.ports
