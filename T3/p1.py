from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from mininet.topo import Topo

## create a Net class to create a topology that uses 4 switches
## and each switch has 2 hosts. And the host must be able to
## ping to every other host in the network.
class Net( Topo ):
	def __init__( self ):
		Topo.__init__( self )
		mac = "00:00:00:00:00:0"
		h1 = self.addHost( 'h1' , mac = mac+'1')
		h2 = self.addHost( 'h2' , mac = mac+'2')
		h3 = self.addHost( 'h3' , mac = mac+'3')
		h4 = self.addHost( 'h4' , mac = mac+'4')
		h5 = self.addHost( 'h5' , mac = mac+'5')
		h6 = self.addHost( 'h6' , mac = mac+'6')
		h7 = self.addHost( 'h7' , mac = mac+'7')
		h8 = self.addHost( 'h8' , mac = mac+'8')

		s1 = self.addSwitch( 's1' )
		s2 = self.addSwitch( 's2' )
		s3 = self.addSwitch( 's3' )
		s4 = self.addSwitch( 's4' )

		self.addLink( s1, s2 , 12, 21)
		self.addLink( s2, s3 , 23, 32)
		self.addLink( s3, s4 , 34, 43)
		self.addLink( s4, s1 , 41, 14)
		self.addLink( s1, h1 , 1, 11)
		self.addLink( s1, h2 , 2, 12)
		self.addLink( s2, h3 , 3, 13)
		self.addLink( s2, h4 , 4, 14)
		self.addLink( s3, h5 , 5, 15)
		self.addLink( s3, h6 , 6, 16)
		self.addLink( s4, h7 , 7, 17)
		self.addLink( s4, h8 , 8, 18)
			
topos = { 'topo1': (lambda: Net() )}
			
