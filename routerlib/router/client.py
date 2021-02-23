

class RouterClient():

    def __init__(self, neighbors):
        print("in router client")
        print(neighbors)
        self.neighbors = neighbors

    def broadcast_data(self, msg, filter_fn):
        to_broadcast = list(filter(filter_fn, self.neighbors.values()))

    def broadcast_revoke(self, msg, filter_fn):
        to_broadcast = list(filter(filter_fn, self.neighbors.values()))

    def broadcast_update(self, msg, filter_fn):
        to_broadcast = list(filter(filter_fn, self.neighbors.values()))

    def forward_data(self, msg, dest):
        self.transmit(dest, msg)

    def send_table_dump(self, table, dest):
        self.transmit(dest, table)

    def _transmit(self, neighbor, msg):
        pass
