from routerlib.util import pairwise, invert_netmask, ip_to_num, num_to_ip


class ForwardingTable():

    def __init__(self):
        self.entries = []
        # populated with tuple (neighbor, routing_info)

    def visit_update(self, source, dest, msg):
        peer = source.get_addr()
        new_entry = msg.msg
        self.entries.append((source, new_entry))
        self._converge(dest)

    def visit_revoke(self, source, dest, msg):
        revokations = msg.msg
        filtered_entries = self.entries
        for revokation in revokations:
            filtered_entries = filter(
                self._filter_revokation(revokation, source), filtered_entries)
        self.entries = list(filtered_entries)

    def get_route(self, dest):

        with_matching_prefix = filter(
            lambda tuple: self._filter_matching_prefix(tuple[1], dest), self.entries)

        alike = self._get_alike(dest, with_matching_prefix)

        lowest_ip = self._resolve_matches(
            dest, alike, lambda dest, neighbor, candidate: -ip_to_num(neighbor.get_addr()))

        try:
            return lowest_ip[0]
        except IndexError:
            return None

    def get_entries(self):
        formatted = map(lambda tuple: {
            "network": tuple[1]['network'], "peer": tuple[0].get_addr(), "netmask": tuple[1]['netmask']}, self.entries)
        return list(formatted)

    def visit_data(self, source, dest, msg):
        pass

    def visit_dump(self, source, dest, msg):
        print(self)

    def _converge(self, dest):
        print("converging")
        print(self)
        grouped_by_ip = self._group_by(
            dest, self.entries, lambda dest, neighbor, entry: ip_to_num(entry['network']))
        just_converged = False
        has_converged_any = False
        converged_entries = []
        for cur, next in pairwise(grouped_by_ip.items()):
            if just_converged:
                just_converged = False
                continue
            cur_ip, cur_routing = cur
            next_ip, next_routing = next
            cur_neighbor, cur_entry = cur_routing[0]
            next_neighbor, next_entry = next_routing[0]
            cur_netmask_num = ip_to_num(cur_entry['netmask'])
            if cur_neighbor.get_addr() == next_neighbor.get_addr() and self._entries_alike(cur_entry, next_entry) and self._ip_nums_adjacent(cur_ip, next_ip, cur_netmask_num):
                # coalesce and skip next iteration
                network_num = cur_ip if cur_ip < next_ip else next_ip
                netmask_num = ip_to_num(
                    cur_entry['netmask']) + (invert_netmask(cur_netmask_num) + 1)
                new_entry = (cur_neighbor, {
                    'network': num_to_ip(network_num),
                    'netmask': num_to_ip(netmask_num),
                    'localpref': cur_entry['localpref'],
                    'ASPath': cur_entry['ASPath'],
                    'origin': cur_entry['origin'],
                    'selfOrigin': cur_entry['selfOrigin']
                })
                just_converged = True
                has_converged_any = True
                converged_entries.append(new_entry)
            else:
                converged_entries.append(cur_routing)
        if has_converged_any:
            self.entries = converged_entries
            self._converge(dest)  # tail call for recursive converges

    def _ip_nums_adjacent(self, ip_num1, ip_num2, netmask_num):
        return abs(ip_num1 - ip_num2) == invert_netmask(netmask_num) + 1

    def _entries_alike(self, entry1, entry2):
        return (entry1['netmask'] == entry2['netmask'] and entry1['localpref'] == entry1['localpref'] and entry1['origin'] == entry2['origin'] and entry1['selfOrigin'] == entry2['selfOrigin'] and entry1['ASPath'] == entry2['ASPath'])

    def _get_alike(self, dest, entries):

        highest_prefix_matches = self._resolve_matches(
            dest, entries, self._rank_prefix_match)

        local_pref_matches = self._resolve_matches(
            dest, highest_prefix_matches, lambda dest, neighbor, candidate: candidate['localpref'])

        self_origin_matches = self._resolve_matches(
            dest, local_pref_matches, lambda dest, neighbor, candidate: 1 if candidate['selfOrigin'] else 0)

        smallest_as_path = self._resolve_matches(
            dest, self_origin_matches, lambda dest, neighbor, candidate: -len(candidate['ASPath']))

        pref_origin_type = self._resolve_matches(
            dest, smallest_as_path, self._rank_origin_by_type)

        return pref_origin_type

    def _group_by(self, dest, candidates, key):
        cand_precedence = {}
        for candidate in candidates:
            cand_neighbor, cand_entry = candidate
            index = key(dest, cand_neighbor, cand_entry)
            index_mems = cand_precedence.get(index, [])
            index_mems.append(candidate)
            cand_precedence[index] = index_mems
        return cand_precedence

    def _resolve_matches(self, dest, candidates, key):
        grouped = self._group_by(dest, candidates, key)

        _len, highest_prefix_matches = sorted(grouped.items(),
                                              key=lambda pair: pair[0], reverse=True)[0]
        return highest_prefix_matches

    def _rank_prefix_match(self, dest, neighbor, candidate):
        dest_ip_int = ip_to_num(dest)
        netmask_int = ip_to_num(candidate['netmask'])
        match_size = dest_ip_int & netmask_int
        return match_size

    def _rank_origin_by_type(self, dest, neighbor, candidate):
        if candidate['origin'] == 'IGP':
            return 2
        elif candidate['origin'] == 'EGP':
            return 1
        elif candidate['origin'] == 'UNK':
            return 0
        else:
            return -1

    def _filter_matching_prefix(self, entry, dest):
        dest_ip_int = ip_to_num(dest)
        network_int = ip_to_num(entry['network'])
        netmask_int = ip_to_num(entry['netmask'])
        return (dest_ip_int & netmask_int) == (network_int & netmask_int)

    def _filter_revokation(self, revokation, source):
        return lambda routing_tuple: not (revokation['netmask'] == routing_tuple[1]['netmask']
                                          and revokation['network'] == routing_tuple[1]['network']
                                          and source.get_addr() == routing_tuple[0].get_addr())

    def __str__(self):
        printout = "============ROUTING TABLE===========\n"
        for entry in self.entries:
            printout += f"Source: {entry[0].__str__()}; Entry: {entry[1].__str__()}\n"
        printout += "==========END ROUTING TABLE========="
        return printout
