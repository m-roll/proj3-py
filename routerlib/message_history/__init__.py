
class MessageHistory():

    # Save update and revoke messages so we can reconstruct forwarding table
    def __init__(self) -> None:
        self.transmissions = []

    def visit_update(self, source, dest, msg):
        self._append('update', source, dest, msg)

    def visit_revoke(self, source, dest, msg):
        self._append('revoke', source, dest, msg)

    def visit_data(self, source, dest, msg):
        pass

    def visit_dump(self, source, dest, msg):
        pass

    def replay(self, receiver):
        pass

    def _append(self, type, source, dest, msg):
        self.transmissions.append((type, source, dest, msg))
