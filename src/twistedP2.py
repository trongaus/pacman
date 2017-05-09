# twistedP2.py (originally home)
# author: Taylor Rongaus
# due May 1, 2017

import pickle
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.protocols.basic import LineReceiver

class DataConnection(Protocol):

	def __init__(self):
		self.connected = False

	def connectionMade(self):
		self.connected = True
		print("twistedP2 data connection made!!")

	def dataReceived(self, data):
		print("twistedP2 got data")
		d = pickle.loads(data)

	def sendData(self, data):
		print("entered twistedP2 sendData function")
		if self.connected:
			print(type(self))
			#self.transport.write(pickle.dumps(data))

class DataFactory(Factory):
	
	def __init__(self):
		self.myconn = DataConnection()
		print("twistedP2 data factory initialized")

	def buildProtocol(self, addr):
		return self.myconn

reactor.listenTCP(41097, DataFactory())
reactor.run()
