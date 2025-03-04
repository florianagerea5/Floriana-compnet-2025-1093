from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class ThreeRouterNet(Topo):

    def __init__(self):
        super(ThreeRouterNet, self).__init__()
        
        # Create hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Create routers
        r1 = self.addHost('r1')
        r2 = self.addHost('r2')
        r3 = self.addHost('r3')

        # Link hosts to routers
        self.addLink(h1, r1, bw=10, delay='5ms')
        self.addLink(h2, r2, bw=10, delay='5ms')
        self.addLink(h3, r3, bw=10, delay='5ms')

        # Link routers together (full mesh)
        self.addLink(r1, r2, bw=10, delay='5ms')
        self.addLink(r1, r3, bw=10, delay='50ms')
        self.addLink(r2, r3, bw=10, delay='5ms')

def configure_routing(net):
  # Configure IP addresses for hosts and routers (replace with desired IPs)
  net.get('h1').cmd('ifconfig h1-eth0 10.1.0.11/24')
  net.get('h2').cmd('ifconfig h2-eth0 10.2.0.22/24')
  net.get('h3').cmd('ifconfig h3-eth0 10.3.0.33/24')
  net.get('r1').cmd('ifconfig r1-eth0 10.1.0.1/24')
  net.get('r2').cmd('ifconfig r2-eth0 10.2.0.2/24')
  net.get('r3').cmd('ifconfig r3-eth0 10.3.0.3/24')
  
  net.get('r1').cmd('ifconfig r1-eth1 10.4.0.1/24')
  net.get('r2').cmd('ifconfig r2-eth1 10.4.0.2/24')

  net.get('r1').cmd('ifconfig r1-eth2 10.5.0.1/24')
  net.get('r3').cmd('ifconfig r3-eth1 10.5.0.3/24')
  
  net.get('r2').cmd('ifconfig r2-eth2 10.6.0.2/24')
  net.get('r3').cmd('ifconfig r3-eth2 10.6.0.3/24')

  # Enable IP forwarding on routers
  net.get('r1').cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
  net.get('r2').cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
  net.get('r3').cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')

  net.get('h1').cmd('route add default gw 10.1.0.1')  # h1 default gateway
  net.get('h2').cmd('route add default gw 10.2.0.2')  # h2 default gateway
  net.get('h3').cmd('route add default gw 10.3.0.3')  # h3 default gateway  

  # Configure static routes on routers (replace with desired routes)
  # ... (static route configuration remains the same)
  net.get('r1').cmd('route add -net 10.2.0.0/24 gw 10.4.0.2')  # Route to reach h2 through r2
  net.get('r2').cmd('route add -net 10.1.0.0/24 gw 10.4.0.1')  # Route to reach h1 through r1
  
  net.get('r1').cmd('route add -net 10.3.0.0/24 gw 10.5.0.3')  # Route to reach h3 through r3
  net.get('r3').cmd('route add -net 10.1.0.0/24 gw 10.5.0.1')  # Route to reach h1 through r1
  
  net.get('r2').cmd('route add -net 10.3.0.0/24 gw 10.6.0.3')  # Route to reach h3 through r3
  net.get('r3').cmd('route add -net 10.2.0.0/24 gw 10.6.0.2')  # Route to reach h2 through r2

def run():
    topo = ThreeRouterNet()
    net = Mininet(topo=topo, link=TCLink)

    net.start()
    configure_routing(net)
    info(net['r1'].cmd('route'))

    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()
