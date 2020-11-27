import ssl
import socket

from typing import List, Optional, Tuple


def find_headers_in_response(response: bytes,
                             headers: Optional[List[str]] = None) -> List[str]:
    """
    Convert response byte strings to strings and search for requested headers.

    :param response: response byte string
    :param headers: headers to search for. Defaults to ['Server', 'server']
    :return: list of strings, which represent data with requested headers
    """
    if headers is None:
        headers = ['Server', 'server']
    response = response.split(b'\r\n')
    response = filter(None, response)
    response = (str(line, 'utf-8') for line in response)
    return [line for line in response
            if line.split(':')[0] in headers]


def request_server_info_via_http(sock: socket.socket,
                                 address_port_pair: Tuple[str, int],
                                 *args, **kwargs) -> str:
    """
    Send request and acquire headers from response.
    Checks if port is 80.

    :param sock: socket to operate on
    :param address_port_pair: tuple of address string & port
    :param args: positional args to forward to `find_headers_in_response`
    :param kwargs: keyword args to forward to `find_headers_in_response`
    :return: single joined string with \r\n string from `find_headers_in_response`
    """
    address, port = address_port_pair
    if port != 80: return ''

    request_str = f"HEAD / HTTP/1.1\r\nHost:{address}\r\n\r\n"
    sock.send(request_str.encode())
    response = sock.recv(4096)
    response = find_headers_in_response(response, *args, **kwargs)
    return '\r\n'.join(response)


def request_server_info_via_https(sock: socket.socket,
                                  address_port_pair: Tuple[str, int],
                                  *args, **kwargs) -> str:
    """
    Wrap socket with ssl, send request and acquire headers
    Checks if port is 443.

    :param sock: socket to operate on
    :param address_port_pair: tuple of address string & port
    :param args: positional args to forward to `find_headers_in_response`
    :param kwargs: keyword args to forward to `find_headers_in_response`
    :return: single joined string with \r\n string from `find_headers_in_response`
    """
    address, port = address_port_pair
    if port != 443: return ''

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with context.wrap_socket(sock, server_hostname=address) as ssl_sock:
        request_str = f"HEAD / HTTP/1.1\r\nHost:{address}\r\n\r\n"
        ssl_sock.send(request_str.encode())
        response = ssl_sock.recv(4096)
    response = find_headers_in_response(response, *args, **kwargs)
    return '\r\n'.join(response)
