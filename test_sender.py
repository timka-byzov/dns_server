from cache_utils import add_cache
from dns_resolver.dns_resolver import DNSResolver

ips = DNSResolver().nslookup("mail.ru")
print(ips)

#
# add_cache("github.com", ["1234.5676.78.8"])
# add_cache("github.com", ["1234.5676.78.8"])
