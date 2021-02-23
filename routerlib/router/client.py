

from routerlib.message import Message


class RouterClient():

    def __init__(self, neighbors):
        self.neighbors = neighbors

    def broadcast_revoke(self, msg, filter_fn):
        to_broadcast = list(filter(filter_fn, self.neighbors.values()))
        for neighbor in to_broadcast:
            self._forward_revoke(neighbor, msg)

    def broadcast_update(self, msg, filter_fn):
        to_broadcast = list(filter(filter_fn, self.neighbors.values()))
        for neighbor in to_broadcast:
            self._forward_update(neighbor, msg)

    def _forward_update(self, neighbor, msg):
        msg.source = neighbor.get_my_router_addr()
        msg.dest = neighbor.get_addr()
        self._transmit(neighbor, msg)

    def _forward_revoke(self, neighbor, msg):
        msg.source = neighbor.get_my_router_addr()
        msg.dest = neighbor.get_addr()
        self._transmit(neighbor, msg)

    def forward_data(self, neighbor, msg):
        self._transmit(neighbor, msg)

    def send_table_dump(self, table, dest):
        src = dest.get_my_router_addr()
        dest = dest.get_addr()
        msg = Message('table', src, dest, table)
        self._transmit(dest, msg)

    def _transmit_many(self, neighbors, msg):
        for neighbor in neighbors:
            self._transmit(neighbor, msg)

    def _transmit(self, neighbor, msg):
        neighbor.transmit(msg)
