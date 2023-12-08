from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether

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
        return pkt.__class__(bytes(pkt))

    def update_layer_2(pkt, src=None, dst=None):
        pkt = pkt.copy()

        pkt[IP].ttl = pkt[IP].ttl - 1

        pkt[Ether].src = None
        pkt[Ether].dst = None
        return checksum_recalc(pkt)

    def handle_internal(pkt):
        new = update_layer_2(pkt)
        sendp(new, iface=external_interface)

    def handle_external(pkt):
        new = update_layer_2(pkt)
        sendp(new, iface=internal_interface)

    def is_http_request(pkt):
        return TCP in pkt and pkt[TCP].dport == 80

    def is_http_response(pkt):
        return TCP in pkt and pkt[TCP].sport == 80

    def print_http_payload(pkt):
        print('http package sniffed')
        if Raw in pkt:
            payload = pkt[Raw].load
            print("HTTP payload:", payload)

    def handle(pkt):
        if sent(pkt):
            return

        if is_http_request(pkt):
            print_http_payload(pkt)

        if is_http_response(pkt):
            print(print_http_payload(pkt))

        if pkt.sniffed_on == internal_interface:
            handle_internal(pkt)
        elif pkt.sniffed_on == external_interface:
            handle_external(pkt)

    sniff(iface=[internal_interface, external_interface], filter='ip', prn=handle)

if __name__ == '__main__':
    main()
