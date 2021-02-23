

class RouterClient():

    def __init__(self, neighbors):
        self.neighbors = neighbors

    def broadcast_data(self, msg, filter_fn):
        to_broadcast = list(filter(filter_fn, self.neighbors.values()))
        self._transmit_many(to_broadcast, msg)

    def broadcast_revoke(self, msg, filter_fn):
        to_broadcast = list(filter(filter_fn, self.neighbors.values()))
        self._transmit_many(to_broadcast, msg)

    def broadcast_update(self, msg, filter_fn):
        to_broadcast = list(filter(filter_fn, self.neighbors.values()))
        self._transmit_many(to_broadcast, msg)

    def forward_data(self, msg, dest):
        self._transmit(dest, msg)

    def send_table_dump(self, table, dest):
        self._transmit(dest, table)

    def _transmit_many(self, neighbors, msg):
        for neighbor in neighbors:
            self._transmit(neighbor, msg)

    def _transmit(self, neighbor, msg):
        print(f"Would have transmitted {msg} to {neighbor.get_addr()}")
