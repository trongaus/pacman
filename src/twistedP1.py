# twistedP1.py (originally home)
# author: Taylor Rongaus
# due May 1, 2017

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

class DataConnection(Protocol):

	def connectionMade(self):
		print("home data connection made!!")

	def dataReceived(self, data):
		pass

class DataFactory(Factory):
	
	def __init__(self):
		self.myconn = DataConnection()

	def buildProtocol(self, addr):
		return self.myconn


#commfact = CommandFactory()
#reactor.listenTCP(40097, commfact)
#reactor.run()
