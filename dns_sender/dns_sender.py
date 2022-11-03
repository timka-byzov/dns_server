import socket

from dns_response.dns_response import DNSResponse
from dns_sender.dns_sender_utils import *


class DNSSender:
    def __init__(self, address: str, port: int = 53, recursive: bool = False):
        self.address = address
        self.port = port
        self.recursive = recursive

    def make_request(self, domain_name: str) -> DNSResponse:
        message = form_dns_message(domain_name)
        bin_data, _ = send_udp_message(message, self.address, self.port)
        return DNSResponse(bin_data)
