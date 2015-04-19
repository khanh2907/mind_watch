from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

from telnetlib import Telnet



class MindWaveClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        tn = Telnet('localhost',13854)
        tn.write('{"enableRawOutput": %s, "format": "Json"}' % (['false','true'][False],))
        i = tn.read_until('\r')
        print("telnet open")

        def hello():            
            self.sendMessage(tn.read_until('\r').encode('utf8'))
            self.factory.reactor.callLater(0.001, hello)

        # start sending messages every second ..
        hello()

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory("ws://localhost:8080", debug=False)
    factory.protocol = MindWaveClientProtocol

    reactor.connectTCP("127.0.0.1", 8080, factory)
    reactor.run()






