

class RouterClient():

    def __init__(self, neighbors):
        print("in router client")
        print(neighbors)
        self.neighbors = neighbors

    def broadcast_data(self, msg, filter_fn):
        to_broadcast = list(filter(filter_fn, self.neighbors.values()))
        print(f'should be broadcasting data {msg}')

    def broadcast_revoke(self, msg, filter_fn):
        to_broadcast = list(filter(filter_fn, self.neighbors.values()))
        print(f'should be broadcasting revokation {msg}')

    def broadcast_update(self, msg, filter_fn):
        to_broadcast = list(filter(filter_fn, self.neighbors.values()))
        print(f'should be broadcasting update {msg}')

    def forward_data(self, msg, dest):
        self.transmit(dest, msg)

    def send_table_dump(self, table, dest):
        self.transmit(dest, table)
        print('should be dumping table')

    def _transmit(self, neighbor, msg):
        pass
