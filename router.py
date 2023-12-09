from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
from util.bad_words import spot_profanity, filter_profanity

def main():
    internal_interface = 'r-eth0'
    external_interface = 'r-eth1'

    def mac(interface):
        return get_if_hwaddr(interface)

    def ip(interface):
        return get_if_addr(interface)

    def sent(pkt):
        if pkt[Ether].src == mac(pkt.sniffed_on):
            return True
        return False

    def checksum_recalc(pkt):
        del pkt[IP].chksum
        del pkt[IP].payload.chksum
        if TCP in pkt:
            print('deleting tcp checksum')
            del pkt[TCP].chksum # added layer 4 chksum recalc
        return pkt.__class__(bytes(pkt))

    def update_layer_2(pkt, src=None, dst=None):
        pkt = pkt.copy()

        pkt[IP].ttl = pkt[IP].ttl - 1

        pkt[Ether].src = None
        pkt[Ether].dst = None

        return checksum_recalc(pkt)

    def handle_internal(pkt):
        new = update_layer_2(pkt)
        sendp(new, iface=external_interface, verbose=False)

    def handle_external(pkt):
        new = update_layer_2(pkt)
        sendp(new, iface=internal_interface, verbose=False)

    def is_http_request(pkt):
        return TCP in pkt and pkt[TCP].dport == 80

    def is_http_response(pkt):
        return TCP in pkt and pkt[TCP].sport == 80
    
    def has_http_payload(pkt):
        return Raw in pkt

    def get_http_payload(pkt):
        return pkt[Raw].load

    def convert_load_to_string(load):
        return load.decode('utf-8')

    def print_http_payload(pkt):
        print(f"http package sniffed on \
            {'internal' if pkt.sniffed_on == internal_interface else 'external'} \
            side with content: {convert_load_to_string(get_http_payload(pkt))}\n", end='\n\n')
        
    def handle_profanity(pkt, mode='block'):
        if mode == 'block':
            return spot_profanity(convert_load_to_string(get_http_payload(pkt))), 'Profanity blocked'
        elif mode == 'filter':
            return spot_profanity(convert_load_to_string(get_http_payload(pkt))), filter_profanity(get_http_payload(pkt))


    def adjust_http_content_length(pkt, new_payload):
        if Raw in pkt:
            http_payload = pkt[Raw].load.decode('utf-8')
            headers, body = http_payload.split("\r\n\r\n", 1)

            # Modify the body here (new_payload should be a string)
            body = new_payload

            # Update Content-Length
            headers_lines = headers.split("\r\n")
            for i, line in enumerate(headers_lines):
                if line.startswith("Content-Length:"):
                    headers_lines[i] = "Content-Length: " + str(len(body))
                    break

            new_http_payload = "\r\n".join(headers_lines) + "\r\n\r\n" + body
            pkt[Raw].load = new_http_payload.encode('utf-8')

        return pkt


    def handle(pkt):
        if sent(pkt):
            return

        if is_http_request(pkt):
            if has_http_payload(pkt):
                print_http_payload(pkt)

        if is_http_response(pkt):
            if has_http_payload(pkt):
                print(get_http_payload(pkt))
                contains_profanity, filtered_content = handle_profanity(pkt, mode='filter')
                print(f"Contains profanity: {contains_profanity}")
                print(f"Filtered content: {filtered_content}")


        if pkt.sniffed_on == internal_interface:
            handle_internal(pkt)
        elif pkt.sniffed_on == external_interface:
            handle_external(pkt)
    
    sniff(iface=[internal_interface, external_interface], filter='ip', prn=handle)


if __name__ == '__main__':
    main()
