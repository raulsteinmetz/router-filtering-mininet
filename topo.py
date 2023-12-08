from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.topo import Topo
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class BasicTopo(Topo):
    def build(self, **_opts):
        # Create switch and router
        sw1 = self.addSwitch('sw1', cls=OVSBridge)
        router = self.addHost('r', ip=None)

        # Create host and server
        host1 = self.addHost('h1', ip='10.1.1.1/24', defaultRoute='via 10.1.1.254')
        server1 = self.addHost('server1', ip='10.1.2.1/24', defaultRoute='via 10.1.2.254')

        # Add links for the new topology
        self.addLink(host1, router, intfName2='r-eth0', params2={'ip': '10.1.1.254/24'})
        self.addLink(router, sw1, intfName2='r-eth1', params2={'ip': '10.1.2.254/24'})
        self.addLink(server1, sw1)

def run():
    "Simplified network setup"
    net = Mininet(topo=BasicTopo(), controller=None)
    net.get('server1').cmd('iperf -s -p 8888 &')

    net.get('r').cmd('sudo sysctl net.ipv4.ip_forward=1')
    net.get('r').cmd('iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP')
        
    for _, v in net.nameToNode.items():
        for itf in v.intfList():
            v.cmd('ethtool -K ' + itf.name + ' tx off rx off')

    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
