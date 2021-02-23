from routerlib.router.client import RouterClient
from routerlib.message_history import MessageHistory
from routerlib.neighbors import Neighbors
from routerlib.forwarding_table import ForwardingTable


class MessageHandler():

    def __init__(self):
        self.router_client = RouterClient()
        self.forwarding_table = ForwardingTable()
        self.message_history = MessageHistory()

    def handle_message(self, srcif, message):
        message.dispatch(self.message_history, srcif)
        message.dispatch(self.forwarding_table, srcif)
        message.dispatch(self, srcif)

    def visit_update(self, source, msg):
        self.router_client.broadcast(msg, self._filter_source(source))

    def visit_revoke(self, source, msg):
        self.router_client.broadcast(msg, self._filter_source(source))

    def visit_data(self, source, dest, msg):
        self.router_client.broadcast(msg)
        pass

    def visit_dump(self, source, dest, msg):
        self.router_client.send_table_dump(
            self.forwarding_table.get_entries(), source)

    def _filter_source(self, source):
        return self._all_neighbors_but_sender(source) if source.type == "cust" else self._all_customers_but_sender(source)

    def _all_neighbors_but_sender(self, source):
        return lambda neighbor: neighbor.get_addr() == source.get_addr()

    def _all_customers_but_sender(self, source):
        return lambda neighbor: neighbor.get_addr() == source.get_addr() and neighbor.type == "cust"
