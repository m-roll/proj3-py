
class ForwardingTable():

    def __init__(self):
        self.entries = []

    def visit_update(self, source, dest, msg):
        neighbor = source.get_addr()
        netmask = msg.msg['netmask']
        peer = msg.msg['network']
        new_entry = {'network': neighbor, 'netmask': netmask, 'peer': peer}

    def visit_revoke(self, source, dest, msg):
        revokations = msg.msg
        filtered_entries = self.entries
        for revokation in revokations:
            filtered_entries = filter(
                self._filter_revokation(revokation, source), filtered_entries)

    def get_entries(self):
        return self.entries

    def visit_data(self, source, dest, msg):
        pass

    def visit_dump(self, source, dest, msg):
        pass

    def _filter_revokation(self, revokation, source):
        return lambda table_entry: not (revokation['netmask'] == table_entry['netmask']
                                        and revokation['network'] == table_entry['network']
                                        and source.get_addr() == table_entry['peer'])
