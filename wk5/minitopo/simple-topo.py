from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink

class SingleSwitchTopology(Topo):
  def build(self, n = 2):
    switch = self.addSwitch('s1')
    for i in range(n):
      host = self.addHost(f'h{i}')
      self.addLink(host, switch)

def main():
  topo = SingleSwitchTopology()
  net = Mininet(topo = topo, link=TCLink)
  net.start()
  CLI(net)
  net.stop()

if __name__ == '__main__':
  main()