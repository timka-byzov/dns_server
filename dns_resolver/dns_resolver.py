from dns_resolver.dns_resolver_utils import retry_nslookup, get_ipv4s

from dns_sender.dns_sender import DNSSender


class DNSResolver:
    @retry_nslookup(["198.41.0.4", "192.36.148.17", "192.58.128.30", "193.0.14.129", "199.7.83.42"])
    def nslookup(self, domain_name, root_server_ip) -> list[str] or None:

        # from_cache = get_from_cache(domain_name)
        # if from_cache is not None:
        #     return from_cache

        curr_ip = root_server_ip
        while True:
            response = DNSSender(curr_ip, recursive=False).make_request(domain_name)

            if response.flags[0] & 0x04:  # server is authority for domain
                # add_cache(domain_name, response.answer_records)
                return get_ipv4s(response.answer_records)

            else:
                curr_ip = get_ipv4s(response.additional_records)[0]
