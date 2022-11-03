import datetime
import json


def make_cache_data(data: list[dict]):
    cache_data = []
    for record in data:
        expire_in = datetime.datetime.now() + datetime.timedelta(seconds=record["ttl"])
        cache_data.append({"ip": record["name_server"], "expire_in": expire_in})

    return cache_data


def add_cache(domain_name: str, data: list[dict]):
    with open('cache.json', 'w') as cache_file:
        cache_dict = json.load(cache_file)
        cache_dict[domain_name] = str(make_cache_data(data))
        json.dump(cache_dict, cache_file)


def get_cache(domain_name: str):
    open('cache.json').close()
    with open('cache.json', 'r', encoding="utf-8") as cache_file:
        cache = json.load(cache_file)

        if domain_name not in cache:
            return None

        return cache[domain_name]


def get_from_cache(domain_name: str):
    cache = get_cache(domain_name)

    if cache is None:
        return None

    for record in cache:
        if record["expire_in"] < datetime.datetime.now():
            break

    else:
        return make_data_from_cache(cache)


def make_data_from_cache(cache: list[dict]):
    return [record["ip"] for record in cache]
