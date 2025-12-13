#script om auto vote uit te voeren

from threading import *
from urllib import *
import time

def performvote(z):
        print "now performing query " + str(z)
        data = "input1=" + str(z) + "&submit=submit"
        print "data set to " + data
        x = urlopen("http://jayke.ulyssis.be/testpage.php",data)
        print "======================================="
        print x.read()

def timerhook(x):
        print "we zitten in timerhook " + str(x)
        performvote(x)
        y = x + 1
        time.sleep(5)
        timerhook(y)


timerhook(1)
