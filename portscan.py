import argparse
import ipaddress
import sys

from itertools import product
from multiprocessing.pool import Pool

from connector import Connector
from request_utils import request_server_info_via_http, request_server_info_via_https


DEFAULT_CHUNKSIZE = 5
DEFAULT_TIMEOUT = 0.001


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
    parser.add_argument('-r', '--request', action='store_true',
                        help="Try to request server info. Has no effect if"
                             "neither 80 or 443 are used as `ports` arguments")
    parser.add_argument('-d', '--debug', action='store_true',
                        help="Do not suppress stack trace")
    args = parser.parse_args()

    # Suppress stack trace when throwing an exception - somewhat console style errors
    if not args.debug: sys.tracebacklimit = 0

    address_range = ipaddress.ip_network(args.range).hosts()
    address_range = map(str, address_range)
    address_port_pairs = product(address_range, args.ports)
    connect_function = Connector(args.timeout,
                                 [request_server_info_via_http,
                                  request_server_info_via_https]
                                 if args.request else None)

    with Pool(args.workers) as p:
        results = p.imap_unordered(connect_function,
                                   address_port_pairs,
                                   chunksize=args.chunksize)
        for (address, port), cb_results in filter(None, results):
            print(f"{address} {port} OPEN")
            if cb_results:
                for res in cb_results:
                    print(res)
