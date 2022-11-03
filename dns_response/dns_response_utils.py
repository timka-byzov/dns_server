def get_name(byte_num, bin_request):
    begin_byte = byte_num

    while bin_request[byte_num] != 0:  # имя кончается на 0
        byte_num += 1
    byte_num += 1

    if bin_request[begin_byte] > 63:  # ссылка
        return 'ref', byte_num - 1

    return bin_request[begin_byte:byte_num].decode('utf-8'), byte_num


def parse_dns_query(byte_num, bin_request):
    query = {}
    query['name'], byte_num = get_name(byte_num, bin_request)
    query['type'] = bin_request[byte_num: byte_num + 2]
    byte_num += 2
    query['class'] = bin_request[byte_num: byte_num + 2]
    byte_num += 2

    return query, byte_num


def parse_dns_records(byte_num, bin_request, records_count):
    records = []

    for rr_num in range(records_count):
        record = dict()
        record['name'], byte_num = get_name(byte_num, bin_request)

        record['type'] = bin_request[byte_num:byte_num + 2]
        byte_num += 2

        record['class'] = bin_request[byte_num:byte_num + 2]
        byte_num += 2

        record['ttl'] = int.from_bytes(bin_request[byte_num: byte_num + 4], byteorder='big')
        byte_num += 4

        record['data_len'] = int.from_bytes(bin_request[byte_num:byte_num + 2], byteorder='big')
        byte_num += 2

        record['name_server'] = bin_request[byte_num:byte_num + record['data_len']]
        byte_num += record['data_len']

        records.append(record)

    return records, byte_num
