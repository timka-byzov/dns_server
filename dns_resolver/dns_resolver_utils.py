import time
from datetime import datetime

from cache_utils import get_cache


def retry_nslookup(root_ip_addresses_to_try: list[str]):
    def retry(func):
        def _wrapper(*args, **kwargs):
            for address in root_ip_addresses_to_try:
                try:
                    res = func(*args, address, **kwargs)
                except:
                    time.sleep(2)
                else:
                    return res

        return _wrapper

    return retry


def get_ipv4s(records: dict):
    return [normalize_ip(record["name_server"]) for record in records if record['data_len'] == 4]


def normalize_ip(byte_ip):
    return '.'.join(str(x) for x in byte_ip)
