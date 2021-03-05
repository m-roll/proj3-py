from routerlib.message import MessageEncoder
from routerlib.router.client import RouterClient
from routerlib.message_history import MessageHistory
from routerlib.neighbors import Neighbors
from routerlib.forwarding_table import ForwardingTable
import json


class MessageHandler():

    def __init__(self, neighbors, _as):
        self.router_client = RouterClient(neighbors, int(_as))
        self.forwarding_table = ForwardingTable()
        self.message_history = MessageHistory()

    def handle_message(self, neighbor, message):
        dest = message.dest
        # print(f'Received message: {json.dumps(message, cls=MessageEncoder)}')
        message.dispatch(self.message_history, neighbor, dest)
        message.dispatch(self.forwarding_table, neighbor, dest)
        message.dispatch(self, neighbor, dest)

    def visit_update(self, source, dest, msg):
        self.router_client.broadcast_update(msg, self._filter_source(source))

    def visit_revoke(self, source, dest, msg):
        print(dest, msg)
        self.router_client.broadcast_revoke(msg, self._filter_source(source))

    def visit_data(self, source, dest, msg):
        # self.router_client.forward_data(msg, self._filter_source(source))
        routing_tuple = self.forwarding_table.get_route(dest)
        if routing_tuple is not None:
            (route_neighbor, routing_info) = routing_tuple
            self.router_client.forward_data(route_neighbor, msg)
        # noroute otherwise

    def visit_dump(self, source, dest, msg):
        self.router_client.send_table_dump(
            self.forwarding_table.get_entries(), source)

    def _filter_source(self, source):
        return self._all_neighbors_but_sender(source) if source.type == "cust" else self._all_customers_but_sender(source)

    def _all_neighbors_but_sender(self, source):
        return lambda neighbor: neighbor.get_addr() != source.get_addr()

    def _all_customers_but_sender(self, source):
        return lambda neighbor: neighbor.get_addr() != source.get_addr() and neighbor.type == "cust"
