import socket
import struct


class ForwardingTable():

    def __init__(self):
        self.entries = []

    def visit_update(self, source, dest, msg):
        peer = source.get_addr()
        new_entry = msg.msg
        self.entries.append(new_entry)

    def visit_revoke(self, source, dest, msg):
        revokations = msg.msg
        filtered_entries = self.entries
        for revokation in revokations:
            filtered_entries = filter(
                self._filter_revokation(revokation, source), filtered_entries)

    def get_route(self, dest):
        # remove any without matching prefix
        with_matching_prefix = filter(
            lambda entry: self._filter_matching_prefix(entry, dest), self.entries)

        highest_prefix_matches = self._resolve_matches(
            dest, with_matching_prefix, self._rank_prefix_match)

        self_origin_matches = self._resolve_matches(
            dest, highest_prefix_matches, lambda dest, candidate: 1 if candidate['selfOrigin'] else 0)

        smallest_as_path = self._resolve_matches(
            dest, self_origin_matches, lambda dest, candidate: -len(candidate['ASPath']))

        pref_origin_type = self._resolve_matches(
            dest, smallest_as_path, self._rank_origin_by_type)

        lowest_ip = self._resolve_matches(
            dest, pref_origin_type, lambda dest, candidate: -self._ip_to_num(candidate['network']))

        try:
            return lowest_ip[0]
        except IndexError:
            return None

    def get_entries(self):
        return self.entries

    def visit_data(self, source, dest, msg):
        pass

    def visit_dump(self, source, dest, msg):
        pass

    def _resolve_matches(self, dest, candidates, key):
        cand_precedence = {}
        for candidate in candidates:
            print("CANDIDATE")
            print(candidate)
            index = key(dest, candidate)
            index_mems = cand_precedence.get(index, [])
            index_mems.append(candidate)
            cand_precedence[index] = index_mems
            print(cand_precedence)

        _len, highest_prefix_matches = sorted(candidate.items(),
                                              key=lambda pair: pair[0])[0]
        print(highest_prefix_matches)
        return highest_prefix_matches

    def _rank_prefix_match(self, dest, candidate):
        dest_ip_int = self._ip_to_num(dest)
        netmask_int = self._ip_to_num(candidate['netmask'])
        match_size = dest_ip_int & netmask_int
        return match_size

    def _rank_origin_by_type(self, dest, candidate):
        if candidate['origin'] == 'IGP':
            return 2
        elif candidate['origin'] == 'EGP':
            return 1
        elif candidate['origin'] == 'UNK':
            return 0
        else:
            return -1

    def _filter_matching_prefix(self, entry, dest):
        dest_ip_int = self._ip_to_num(dest)
        network_int = self._ip_to_num(entry['network'])
        netmask_int = self._ip_to_num(entry['netmask'])
        return (dest_ip_int & netmask_int) == (network_int & netmask_int)

    def _ip_to_num(self, ip):
        ip_parts = ip.split(".")
        return (int(ip_parts[0]) << 24) + (int(ip_parts[1]) << 16) + (int(ip_parts[2]) << 8) + int(ip_parts[3])

    def _filter_revokation(self, revokation, source):
        return lambda table_entry: not (revokation['netmask'] == table_entry['netmask']
                                        and revokation['network'] == table_entry['network']
                                        and source.get_addr() == table_entry['peer'])
