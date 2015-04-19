
import sys
import six
import datetime

from twisted.python import log
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.endpoints import serverFromString

from autobahn.wamp import types
from autobahn.twisted.util import sleep
from autobahn.twisted import wamp, websocket
import ConfigParser
import json
from telnetlib import Telnet

from firebase import firebase



class MindwaveComponent(wamp.ApplicationSession):
	"""
	Application code goes here. This is an example component that provides
	a simple procedure which can be called remotely from any WAMP peer.
	It also publishes an event every second to some topic.
	"""

	@inlineCallbacks
	def onJoin(self, details):

		namespace = self.app_config['namespace']
		do_raw = self.app_config['raw'].lower()=='true'

		firebase_server = firebase.FirebaseApplication('https://amber-fire-3917.firebaseio.com')

		def send(key,d):
			return self.publish(namespace+u'.queue.'+key,d) and 1 or 0

		def blink(d):
			return send('blink',d['blinkStrength'])

		def data(d):
			return send('data',
				[d['eSense']['attention']
				,d['eSense']['meditation']
				,d['eegPower']['lowAlpha']
				,d['eegPower']['highAlpha']
				,d['eegPower']['lowBeta']
				,d['eegPower']['highBeta']
				,d['eegPower']['lowGamma']
				,d['eegPower']['highGamma']
				,d['eegPower']['delta']
				,d['eegPower']['theta']
				])

		def raw(d):
			return send('raw',d['rawEeg'])

		def sendany(d):
			print(d)
			if 'blinkStrength' in d:
				return blink(d)
			if 'eegPower' in d:
				return data(d)
			if 'rawEeg' in d:
				return raw(d)
			return None

		if self.app_config['debug'].lower()=='true':
			print('debug mode.')
			counter = 0
			while True:
				send('debug', counter)
				#print("Published event.")
				counter += 1
				yield sleep(1)
		else:
			tn = Telnet('localhost',13854)
			tn.write('{"enableRawOutput": %s, "format": "Json"}' % (['false','true'][do_raw],))
			i = tn.read_until('\r')
			while True:
				# ret = sendany(json.loads(tn.read_until('\r')))
				firebase_server.post('/mindwave', json.loads(tn.read_until('\r')))
				yield sleep(0.001)

def start_server(config):
	log.startLogging(sys.stdout)
	router_factory = wamp.RouterFactory()
	session_factory = wamp.RouterSessionFactory(router_factory)
	component_config = types.ComponentConfig(realm=config['realm'])
	component_session = MindwaveComponent(component_config)
	component_session.app_config = config
	session_factory.add(component_session)
	transport_factory = websocket.WampWebSocketServerFactory(session_factory,debug=False,debug_wamp=False)
	server = serverFromString(reactor, config['server_string'])
	server.listen(transport_factory)
	reactor.run()

def main():
	print(len(sys.argv))
	print(sys.argv)
	if 1<len(sys.argv)<4 and sys.argv[1][-4:]=='.cfg':
		configpath = sys.argv[1]
		configsection = (sys.argv[2:] or ['DEFAULT'])[0]
		configreader = ConfigParser.ConfigParser()
		configreader.read(configpath)
		config=dict(configreader.items(configsection))
		start_server(config)

if __name__ == '__main__':
	main()
