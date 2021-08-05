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

		# Link entre switches
		self.addLink( s1, s4 , 21, 34)
		self.addLink( s4, s3 , 24, 33)
		self.addLink( s3, s2 , 23, 32)
		self.addLink( s2, s1 , 22, 31)

		# Link entre hosts
		self.addLink( h1, s1 , 1, 11)
		self.addLink( h2, s1 , 2, 12)

		self.addLink( h3, s2 , 3, 13)
		self.addLink( h4, s2 , 4, 14)

		self.addLink( h5, s3 , 5, 15)
		self.addLink( h6, s3 , 6, 16)
		
		self.addLink( h7, s4 , 7, 17)
		self.addLink( h8, s4 , 8, 18)
			
topos = { 'topo1': (lambda: Net() )}
			
