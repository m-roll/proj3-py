

class Message():

    def __init__(self, type, source, dest, msg) -> None:
        self.type = type
        self.source = source
        self.dest = dest
        self.msg = msg

    def dispatch(self, receiver, neighbor_from, dest):
        visit_callback = None
        if self.type == "update":
            visit_callback = receiver.visit_update
        elif self.type == "revoke":
            visit_callback = receiver.visit_revoke
        elif self.type == "data":
            visit_callback = receiver.visit_data
        elif self.type == "dump":
            visit_callback = receiver.visit_dump
        visit_callback(neighbor_from, dest, self)
