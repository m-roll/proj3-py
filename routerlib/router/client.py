

from routerlib.message import Message


class RouterClient():

    def __init__(self, neighbors, _as):
        self.neighbors = neighbors
        self._as = _as

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
        msg.msg = self._incr_path(msg.msg)
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
        neighbor = self.neighbors[dest]
        msg = Message('table', src, dest, table)
        self._transmit(neighbor, msg)

    def _transmit_many(self, neighbors, msg):
        for neighbor in neighbors:
            self._transmit(neighbor, msg)

    def _transmit(self, neighbor, msg):
        neighbor.transmit(msg)

    def _incr_path(self, msg):
        print("**************")
        print('msg before append')
        print(msg)
        last = msg['ASPath'][-1]
        if not self._as == last:
            msg['ASPath'] = msg['ASPath'].append(self._as)
            print("new AS chain after append")
            print(msg)
        return msg
