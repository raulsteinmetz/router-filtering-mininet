from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
from util.bad_words import bad_words_filter

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
            del pkt[TCP].chksum # added layer 4 chksum recalc
        return pkt.__class__(bytes(pkt))

    def update_layer_2(pkt, src=None, dst=None):
        pkt = pkt.copy()

        pkt[IP].ttl = pkt[IP].ttl - 1

        pkt[Ether].src = None
        pkt[Ether].dst = None

        return checksum_recalc(pkt)

    def is_http_request(pkt):
        return TCP in pkt and pkt[TCP].dport == 80

    def is_http_response(pkt):
        return TCP in pkt and pkt[TCP].sport == 80
    
    def has_http_payload(pkt):
        return Raw in pkt

    def get_http_payload(pkt):
        return pkt[Raw].load
        
    def handle_profanity(pkt):
        return bad_words_filter('./badwords.txt', get_http_payload(pkt).decode('utf-8'))
    

    pkt_buffer = []

    def handle(pkt):
        if sent(pkt):
            return

        ok = False
        is_http = False
        http_modified = False

        if is_http_response(pkt):
            is_http = True
            if has_http_payload(pkt):

                if 'OK' in get_http_payload(pkt).decode('utf-8'):
                    ok = True
                    pkt_buffer.append(pkt)
                else:
                    http_payload_str = get_http_payload(pkt).decode('utf-8')
                    contains_profanity, filtered_content = handle_profanity(pkt)
                    if contains_profanity: 
                        http_modified = True
                        pkt[Raw].load = filtered_content

        
        if pkt.sniffed_on == internal_interface:
            new = update_layer_2(pkt)
            sendp(new, iface=external_interface, verbose=False)
        elif pkt.sniffed_on == external_interface and is_http and not ok:
            if len(pkt_buffer) > 0:
                ok_pkt = pkt_buffer.pop()
                ok_pkt = update_layer_2(ok_pkt)
                sendp(ok_pkt, iface=internal_interface, verbose=False)

            new = update_layer_2(pkt)
            sendp(new, iface=internal_interface, verbose=False)
        else:
            new = update_layer_2(pkt)
            sendp(new, iface=internal_interface, verbose=False)

    
    sniff(iface=[internal_interface, external_interface], filter='ip', prn=handle)


if __name__ == '__main__':
    main()
