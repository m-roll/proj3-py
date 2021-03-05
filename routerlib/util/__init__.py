import itertools

# recipe from https://docs.python.org/3/library/itertools.html#recipes
# Bad design but I'm shoving a bunch of random functions in this util
#     module lmao.


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def invert_netmask(netmask):
    netmask ^ ip_to_num("255.255.255.255")


def ip_to_num(ip):
    ip_parts = ip.split(".")
    return (int(ip_parts[0]) << 24) + (int(ip_parts[1]) << 16) + (int(ip_parts[2]) << 8) + int(ip_parts[3])


def num_to_ip(ip_num):
    return '.'.join([str(ip_num >> (ii << 3) & 0xFF)
                     for ii in range(4)[::-1]])
