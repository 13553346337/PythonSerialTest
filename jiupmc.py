#!/usr/bin/python
# -*- coding: utf-8 -*
import tornado.web
import tornado.websocket
import tornado.ioloop

import serial
import time

clients = []

serW = serial.Serial('/dev/ttyUSB0', 2400, 7, 'N', 1)
time.sleep(0.1)
serW = serial.Serial("/dev/ttyUSB0", 1200, 7, 'N', 1)


def ss(rr):
    ta = ord(rr)
    if ta & 128 == 128 :
        return chr(ta ^ 128)
    else:
        return rr


def readData():
    if serW.inWaiting() >= 17 :
        recvW = ''.join(map(ss, serW.read(17)))
        tmp = recvW.find(' ')
        if tmp == -1 :
            pass
        elif tmp == 3 and len(clients) :
            #print recvW[4:10]
            clients[0].write_message(recvW[4:10])
        elif tmp != 3 :
            serW.read(17 + tmp - 3)


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
