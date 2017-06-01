#!/usr/bin/python
# -*- coding: utf-8 -*

#import tornado.web
import tornado.ioloop
import urllib2

def test():
    try:
        re = urllib2.urlopen("http://192.168.1.245/sj/transfer",timeout=2)
    except urllib2.HTTPError:
        pass

if __name__ == '__main__':
    #test()
    tornado.ioloop.PeriodicCallback(test, 2000).start()
    tornado.ioloop.IOLoop.instance().start()
