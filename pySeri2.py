#!/usr/bin/python
# -*- coding: utf-8 -*
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.httputil
import tornado.escape
import tornado.httpclient

import serial
import time

clients = []
serW = serial.Serial('/dev/ttyUSB0',9600)
#serC = serial.Serial('/dev/ttyUSB1',2400)
time.sleep(0.1)
serW = serial.Serial("/dev/ttyUSB0", 2400)
#serC = serial.Serial('/dev/ttyUSB1',9600)
aa = [0,]
bb = [0,]
def readData():
    if serW.inWaiting() >= 8 :
        recvW = serW.read( 8 )
        resetmp = recvW.find('=')
        if resetmp == 0 and len(clients) : # and bb[0] == 0 :
            #print recvW[5:0:-1]
            clients[0].write_message('WD-%s' % recvW[5:0:-1])
        elif resetmp == -1 :
            pass
        elif resetmp > 0 :
            serW.read( resetmp + 8 )
        #bb[0]=(bb[0]+1)%2

"""
def readData():
#    print bb[0]
    if serW.inWaiting() >= 13 :
        recvW = serW.read( 13 )
        resetmp = recvW.find('+')
        if resetmp == 0 and len(clients) and bb[0] == 0 :
            clients[0].write_message('WD-%s' % recvW[2:7])
        elif resetmp == -1 :
            pass
        elif resetmp > 0 :
            serW.read( resetmp + 13 )
        bb[0]=(bb[0]+1)%3
"""

"""
        elif client:
            #for client in clients:
            client.write_message('WD-%s' % recvW[6:0:-1])
"""

def readCard():
    tmpC = serC.inWaiting()
    if aa[0] == 0 and tmpC == 14 :
        recvC = serC.read( 14 )[1:11]
        aa[0] = 4
        clients[0].write_message('CD-%s' % recvC ) #print recvC
    elif aa[0] == 0 :
        if tmpC >0 :
            recvC = serC.read(tmpC)
    else :
        aa[0] -= 1


#class dataHandler(tornado.web.RequestHandler):

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        #print "new client"
        clients.append(self)

    def on_message(self, message):
        pass
        #print message
        #msg=json.loads(message)
        #self.write_message(message)


    def on_close(self):
        clients.remove(self)

    def check_origin(self, origin):
        return True

application = tornado.web.Application([
    (r"/online", WebSocketHandler),
])


def main():
    application.listen(8888)
#    tornado.ioloop.PeriodicCallback(readCard, 100).start()
    tornado.ioloop.PeriodicCallback(readData, 100).start()
    tornado.ioloop.IOLoop.instance().start()

"""
    while True:
        countC = serW.inWaiting()
        if countC >= readBit :
            recvW = serW.read( readBit )
            resetmp = recvW.find('=')
            if resetmp :
                fixPoint(resetmp)
            elif len(clients):
                for client in clients:
                    client.write_message("{'type':'weight','weight':'%s'}" % recvs)
            time.sleep(0.1)
"""

"""
        if countC == 0:
            recvW = serW.read(countC)
#            countW = serW.inWaiting()
#            recvW = serW.read(countW)
            #ser.write(recv)
            # print recv[1:11]
            print  recvW
        serW.flushInput()
#        serW.flushInput()
        time.sleep(0.1)
"""

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if serW != None:
            serW.close()
 #       if serW != None:
 #           serW.close()
