from dns_response.dns_response_utils import parse_dns_records, parse_dns_query


class DNSResponse:
    def __init__(self, bin_request):
        self.transaction_id = bin_request[0:2].decode('utf-8')
        self.flags = bin_request[2:4]
        self.questions = int.from_bytes(bin_request[4:6], byteorder='big')
        self.answer_records_count = int.from_bytes(bin_request[6:8], byteorder='big')
        self.authority_records_count = int.from_bytes(bin_request[8:10], byteorder='big')
        self.additional_records_count = int.from_bytes(bin_request[10:12], byteorder='big')

        byte_num = 12
        self.query, next_byte = parse_dns_query(byte_num, bin_request)
        self.answer_records, next_byte = parse_dns_records(next_byte, bin_request, self.answer_records_count)
        self.authority_records, next_byte = parse_dns_records(next_byte, bin_request, self.authority_records_count)
        self.additional_records, _ = parse_dns_records(next_byte, bin_request, self.additional_records_count)

