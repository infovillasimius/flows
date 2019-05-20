from timeit import default_timer as timer
from graph import *
from queues import *


def dijkstra(g):
    if g.negative:
        return g
    g.initialize()
    my_list = g.nodeList
    start_time = timer()
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
    g.exec_time = timer() - start_time
    return g


def dial_dijkstra(g):
    if g.negative:
        return g
    my_list = g.nodeList
    g.initialize()
    q = CircularQueue(g.C+1)
    q.store(g.s)
    start_time = timer()
    while my_list.__len__() > 0:
        n = q.next()
        if n.labeled is not True:
            my_list.remove(n)
            n.labeled = True
            for a in n.outList:
                dist = a.tail.d + a.cost
                if a.head.d > dist:
                    a.head.d = dist
                    a.head.predecessor = a.tail
                    q.store(a.head)
    g.exec_time = timer() - start_time
    return g


def label_correcting(g):
    g.initialize()
    mindist = -g.nodes_number * g.C
    optcond = False
    start_time = timer()

    while not optcond:
        optcond = True
        for a in g.arcList:
            dist = a.tail.d + a.cost
            if a.head.d > dist:
                a.head.d = dist
                a.head.predecessor = a.tail
                optcond = False
                n = a.head
        if dist < mindist:
            optcond = True
            g.nCycle = n
    g.exec_time = timer() - start_time
    return g


