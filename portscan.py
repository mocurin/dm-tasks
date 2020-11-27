import argparse
import ipaddress
import socket

from itertools import product
from multiprocessing.pool import Pool


DEFAULT_CHUNKSIZE = 5
DEFAULT_TIMEOUT = 0.001

# Workaround for setting connect`s timeout without decorator
# since multiprocessing requires top-level function declarations
conn_timeout = DEFAULT_TIMEOUT


def connect(address_port_pair, timeout=conn_timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        err = s.connect_ex(address_port_pair)
        if not err:
            return address_port_pair
        # return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Investigate network for open ports")
    parser.add_argument('range',
                        help="IP-addresses range")
    parser.add_argument('ports', nargs='+', type=int,
                        help="List of ports")
    parser.add_argument('-w', '--workers', type=int, default=1,
                        help="Number of workers to use")
    parser.add_argument('-c', '--chunksize', type=int, default=DEFAULT_CHUNKSIZE,
                        help="Chunk size to use within process pool`s imap")
    parser.add_argument('-t', '--timeout', type=float, default=DEFAULT_TIMEOUT,
                        help="Socket timeout")
    args = parser.parse_args()

    conn_timeout = args.timeout

    addr_range = ipaddress.ip_network(args.range).hosts()
    addr_range = map(str, addr_range)
    addr_port_pairs_generator = product(addr_range, args.ports)

    with Pool(args.workers) as pool:
        results = pool.imap_unordered(connect,
                                      addr_port_pairs_generator,
                                      chunksize=args.chunksize)
        for addr, port in filter(None, results):
            print(f"{addr} {port} OPEN")
