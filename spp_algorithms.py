import time
from graph import *


def dijkstra(g):
    if g.negative:
        return g

    g.initialize()
    my_list = g.nodeList

    start_time=time.time()

    while my_list.__len__() > 0:
        minor = math.inf
        for i in my_list:
            if i.d < minor:
                n = i
                minor = i.d
        my_list.remove(n)
        for a in n.outList:
            dist = a.tail.d + a.cost
            if a.head.d > dist:
                a.head.d = dist
                a.head.predecessor = a.tail

    g.exec_time=time.time()-start_time

    return g


def label_correcting(g):
    g.initialize()
    mindist=-g.nodes_number*g.C
    optcond=False
    start_time=time.time()
    while not optcond:
        optcond=True
        for a in g.arcList:
            dist=a.tail.d+a.cost
            if a.head.d>dist:
                a.head.d=dist
                a.head.predecessor=a.tail
                optcond=False
                n=a.head
        if dist<mindist:
            optcond=True
            g.nCycle=n
    g.exec_time = time.time() - start_time
    return g

