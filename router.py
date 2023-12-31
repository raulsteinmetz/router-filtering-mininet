from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
from util.bad_words import BadWordsFilter
import argparse

def main(badwords_filter):
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
        return bwfilter.filter(get_http_payload(pkt).decode('utf-8'))
    

    class OkMsg:
        def __init__(self, pkt):
            self.pkt = pkt
            self.ip_src = pkt[IP].src
            self.ip_dst = pkt[IP].dst


    def pop_ok_pkt(ip_src, ip_dst):
        for ok_msg in ok_pkt_buffer:
            if ok_msg.ip_src == ip_src and ok_msg.ip_dst == ip_dst:
                ok_pkt_buffer.remove(ok_msg)
                return ok_msg
        return None           

    ok_pkt_buffer = []

    bwfilter = BadWordsFilter('./badwords.txt')




    def handle(pkt):
        if sent(pkt):
            return

        ok = False
        is_http = False

        if badwords_filter:

            if is_http_response(pkt):
                is_http = True
                if has_http_payload(pkt):

                    if 'OK' in get_http_payload(pkt).decode('utf-8'):
                        ok = True
                        ok_pkt_buffer.append(OkMsg(pkt))
                    else:
                        contains_profanity, filtered_content = handle_profanity(pkt)
                        if contains_profanity: 
                            pkt[Raw].load = filtered_content

        
        if pkt.sniffed_on == internal_interface:
            new = update_layer_2(pkt)
            sendp(new, iface=external_interface, verbose=False)
        elif pkt.sniffed_on == external_interface and is_http and not ok and badwords_filter:
            if len(ok_pkt_buffer) > 0:
                crt_src = pkt[IP].src
                crt_dst = pkt[IP].dst
                ok_pkt = pop_ok_pkt(crt_src, crt_dst).pkt
                ok_pkt = update_layer_2(ok_pkt)
                sendp(ok_pkt, iface=internal_interface, verbose=False)

            new = update_layer_2(pkt)
            sendp(new, iface=internal_interface, verbose=False)
        elif pkt.sniffed_on == external_interface and not badwords_filter:
            new = update_layer_2(pkt)
            sendp(new, iface=internal_interface, verbose=False)

    
    sniff(iface=[internal_interface, external_interface], filter='ip', prn=handle)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filter_badwords', action='store_true', help='enables bad words filter')
    args = parser.parse_args()
    main(args.filter_badwords)
