# twistedP1.py (originally work)
# author: Taylor Rongaus
# due May 1, 2017

import pickle
import main
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.protocols.basic import LineReceiver

class DataConnection(Protocol):

	def __init__(self):
		self.connected = False

	def connectionMade(self):
		self.connected = True
		print("twistedP1 data connection made!!")

	def dataReceived(self, data):
		print("twistedP1 got data")
		d = pickle.loads(data)

	def sendData(self, data):
		print("entered twistedP1 sendData function")
		if self.connected:
			print(type(self))
			self.transport.write(pickle.dumps(data))

class DataFactory(ClientFactory):
   
	def __init__(self):
		self.myconn = DataConnection()
		print("twistedP1 data factory initialized")

	def buildProtocol(self, addr):
		return self.myconn

