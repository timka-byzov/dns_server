import binascii
import socket


class DNSServer:
    def nslookup(self, str_addr):
        bin_data, addr = self.send_udp_message(self.form_dns_message(str_addr),
                                               "193.232.128.6", 53)

        return DNSResponse(bin_data)

    def send_udp_message(self, message, address, port):
        """send_udp_message sends a message to UDP server

        message should be a hexadecimal encoded string
        """
        server_address = (address, port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(message, server_address)
            bin_data, addr = sock.recvfrom(4096)
        finally:
            sock.close()
        return bin_data, addr

    def get_dns_query(self, str_address):
        arr_address = str_address.split('.')
        bin_address = bytes(0)

        for sub_domen in arr_address:
            len_in_bytes = bytes([len(sub_domen)])
            block = len_in_bytes + bytes(sub_domen, 'utf-8')
            bin_address += block

        bin_address += bytes([0])

        req_type = bytes([0x00, 0x0c])
        req_class = bytes([0x00, 0x01])

        return bin_address + req_type + req_class

    def form_dns_message(self, str_address):
        id = bytearray('bb', 'utf-8')
        flags = bytes([0x00, 0x00])
        questions = bytes([0x00, 0x01])
        answer_rrs = bytes([0x00, 0x00])
        authority_rrs = bytes([0x00, 0x00])
        additional_rrs = bytes([0x00, 0x00])

        return id + flags + questions + answer_rrs + authority_rrs + additional_rrs + self.get_dns_query(str_address)


class DNSResponse:
    def __init__(self, bin_request):
        self.transaction_id = bin_request[0:2].decode('utf-8')
        self.flags = bin_request[2:4]
        self.questions = bin_request[4:6]
        self.answer_records_count = int.from_bytes(bin_request[6:8], byteorder='big')
        self.authority_records_count = int.from_bytes(bin_request[8:10], byteorder='big')
        self.additional_records_count = int.from_bytes(bin_request[10:12], byteorder='big')

        byte_num = 12
        self.query, next_byte = self.parse_dns_query(byte_num, bin_request)

        self.authority_records, next_byte = self.parse_records(next_byte, bin_request, self.authority_records_count)

        self.additional_records, _ = self.parse_records(next_byte, bin_request, self.additional_records_count)

    @staticmethod
    def parse_dns_query(byte_num, bin_request):
        query = dict()
        begin_byte = byte_num

        #  имя кончается на 0
        while bin_request[byte_num] != 0:
            byte_num += 1
        byte_num += 1

        query['name'] = bin_request[begin_byte:byte_num].decode('utf-8')
        query['type'] = bin_request[byte_num: byte_num + 2]
        byte_num += 2
        query['class'] = bin_request[byte_num: byte_num + 2]
        byte_num += 2

        return query, byte_num

    @staticmethod
    def parse_records(byte_num, bin_request, records_count):

        records = []

        for rr_num in range(records_count):
            record = dict()
            record['name'] = bin_request[byte_num:byte_num + 2]
            byte_num += 2

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

    @staticmethod
    def normalize_ip(byte_ip):
        return '.'.join(str(x) for x in byte_ip)


sever = DNSServer()
dns_response = sever.nslookup('yandex.ru')

ip = dns_response.additional_records[0]["name_server"]

print(DNSResponse.normalize_ip(ip))