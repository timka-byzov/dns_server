import socket


def send_udp_message(message, address, port):
    server_address = (address, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(message, server_address)
        bin_data, addr = sock.recvfrom(8000)
    finally:
        sock.close()
    return bin_data, addr


def get_dns_query(domain_name):
    req_type = bytes([0x00, 0x01])
    # req_type = bytes([0x00, 0x0c])
    req_class = bytes([0x00, 0x01])

    bin_address = bytes()

    if domain_name != '.':
        arr_address = domain_name.split('.')
        bin_address = bytes(0)

        for sub_domen in arr_address:
            len_in_bytes = bytes([len(sub_domen)])
            block = len_in_bytes + bytes(sub_domen, 'utf-8')
            bin_address += block

    bin_address += bytes([0])

    return bin_address + req_type + req_class


def form_dns_message(domain_name):
    request_id = bytearray('ba', 'utf-8')
    flags = bytes([0x01, 0x00])
    questions = bytes([0x00, 0x01])
    answer_rrs = bytes([0x00, 0x00])
    authority_rrs = bytes([0x00, 0x00])
    additional_rrs = bytes([0x00, 0x00])

    return request_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + get_dns_query(domain_name)
