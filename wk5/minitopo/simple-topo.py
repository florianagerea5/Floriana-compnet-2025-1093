from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink

class SingleSwitchTopology(Topo):
  def build(self, n = 2):
    switch = self.addSwitch('s1')
    for i in range(1, n + 1):
      host = self.addHost('h{i}'.format(i = i))
      self.addLink(switch, host)

topos = { 'simpletopo': SingleSwitchTopology }

# def main():
#   topo = SingleSwitchTopology()
#   net = Mininet(topo = topo)
#   net.start()
#   CLI(net)
#   net.stop()

# if __name__ == '__main__':
#   main()