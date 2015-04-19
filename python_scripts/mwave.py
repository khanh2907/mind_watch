#!/usr/bin/env python

#import thread
#thread.start_new_thread(main,(,))


import sys
import json
from telnetlib import Telnet
from coroutine import coroutine

debug = sys.argv[1:] and sys.argv[1]=='DEBUG' and True or False

firebase_server = firebase.FirebaseApplication('https://amber-fire-3917.firebaseio.com')

def readgenerator(stream):
	i = stream.read_until('\r')
	while True:
		yield json.loads(stream.read_until('\r'))

@coroutine
def payload_printer():
	while True:
		c = (yield)
		print c
		sys.stdout.flush()

@coroutine
def payload_handler(target):
	while True:
		c = (yield)
		target.send(c)

def run(s,callback):
	for i in readgenerator(s):
		if debug:
			print(i)
		callback(i)

def init(tn,raw=False):
	tn.write('{"enableRawOutput": %s, "format": "Json"}' % (['false','true'][raw],))

def auth(tn):
	tn.write('{"appName": "Example", "appKey": "9f54141b4b4c567c558d3a76cb8d715cbde03096"}')

def getConn(host,port):
	return Telnet(host,port)

def main(host='localhost',port=13854,callback=None,raw=False):
	tn = getConn(host,port)
	init(tn,raw)
	run(tn,callable(callback) and callback or payload_printer().send)

if __name__ == '__main__':
	main()
