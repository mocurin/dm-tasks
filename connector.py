import socket

from typing import Callable, List, Optional, Tuple


class Connector:
    def __init__(self,
                 timeout: float,
                 on_connect_callbacks: Optional[List[Callable]] = None):
        """
        Decorator workaround for usage in multiprocessing.Pool`s

        :param timeout: block time on socket connection
        :param on_connect_callbacks: functions to execute over socket & `address_port_pair`
        """
        if on_connect_callbacks is None:
            on_connect_callbacks = []
        self.timeout = timeout
        self.on_connect_callbacks = on_connect_callbacks

    def __call__(self, address_port_pair: Tuple[str, int]):
        """
        Try to establish connection with `address_port_pair` & launch callbacks on success

        :param address_port_pair: tuple of address string & port
        :return: input tuple & callbacks results if connected, None otherwise
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(self.timeout)
            err = sock.connect_ex(address_port_pair)
            if err:
                return None
            sock.settimeout(socket.getdefaulttimeout())
            cb_results = [cb(sock, address_port_pair)
                          for cb in self.on_connect_callbacks]
            cb_results = filter(None, cb_results)
            return address_port_pair, cb_results
