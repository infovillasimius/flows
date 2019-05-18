import time
import math
from graph import *


def dijkstra(g):
    if g.negative:
        return g

    my_list = g.nodeList
    for n in my_list:
        n.d = math.inf
    s = g.s
    s.d = 0

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
