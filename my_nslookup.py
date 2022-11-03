import sys

from dns_resolver.dns_resolver import DNSResolver

if __name__ == "__main__":
    domain_name = sys.argv[1]

    ips = DNSResolver().nslookup(domain_name)
    print(ips)
