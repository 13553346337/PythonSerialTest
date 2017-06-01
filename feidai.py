#!/usr/bin/python
# -*- coding: utf-8 -*
import tornado.web
import tornado.websocket
import tornado.ioloop

import serial
import time

clients = []
#serW = serial.Serial('/dev/ttyUSB0',9600)
time.sleep(0.1)
serW = serial.Serial("/dev/ttyUSB0", 2400,7,"N",1)
aa = [0,]
def readData():
    if serW.inWaiting() >= 9 :
        recvW = serW.read( 9 )
#	print recvW[1:8]
        resetmp = recvW.find('=')
#	print resetmp
        if resetmp == 0  :
            for client in clients :
                client.write_message(recvW[1:8])
	#	client.write_message(u"123321")
                print recvW[1:8]
        #    aa[0] = 0
	#    pass		
        elif resetmp == -1 :
            pass
        else :
            serW.read( resetmp + 9 - 0 )
       #     if aa[0] < 4: 
       #         aa[0] += 1

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        clients.append(self)

    def on_message(self, message):
        pass

    def on_close(self):
        clients.remove(self)

    def check_origin(self, origin):
        return True

application = tornado.web.Application([
    (r"/online", WebSocketHandler),
])


def main():
    application.listen(8888)
    tornado.ioloop.PeriodicCallback(readData, 100).start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if serW != None:
            serW.close()
