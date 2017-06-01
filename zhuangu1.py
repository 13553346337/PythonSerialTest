#!/usr/bin/python
# -*- coding: utf-8 -*
import tornado.web
import tornado.websocket
import tornado.ioloop

import serial
import time

clients = []
serW = serial.Serial('/dev/ttyUSB0',9600)
time.sleep(0.1)
serW = serial.Serial("/dev/ttyUSB0", 2400)
aa = [0,]
def readData():
    if serW.inWaiting() >= 12 :
        recvW = serW.read( 12 )
        resetmp = recvW.find('+')
        if resetmp == 1 and len(clients) :
            clients[0].write_message(recvW[4:8])
        elif resetmp == -1 :
            pass
        else :
            serW.read( resetmp + 12 -1 )

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
