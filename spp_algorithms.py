from timeit import default_timer as timer
from graph import *
from queues import *


def dynamic(g):
    g.initialize()
    if not g.is_ordered:
        return g
    start_time = timer()
    for n in g.nodeList:
        for a in n.outList:
            dist = a.tail.d + a.cost
            if a.head.d > dist:
                a.head.d = dist
                a.head.predecessor = a.tail
    g.exec_time = timer() - start_time
    return g


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


def radix_heap_dijkstra(g):
    if g.negative:
        return g
    my_list = g.nodeList
    g.initialize()
    q = RadixHeap(g.nodes_number*g.C)
    q.store(g.s)
    g.s.labeled = True
    start_time = timer()
    while len(my_list) > 0:
        n = q.next()
        n.labeled = False
        my_list.remove(n)
        for a in n.outList:
            dist = a.tail.d + a.cost
            oldD = a.head.d
            if oldD > dist:
                a.head.d = dist
                a.head.predecessor = a.tail
                if a.head.labeled:
                    q.update(node=a.head, oldD=oldD)
                else:
                    a.head.labeled = True
                    q.store(a.head)
    g.exec_time = timer() - start_time
    return g


def label_correcting(g):
    g.initialize()
    min_dist = -g.nodes_number * g.C
    opt_cond = False
    start_time = timer()

    while not opt_cond:
        opt_cond = True
        for a in g.arcList:
            dist = a.tail.d + a.cost
            if a.head.d > dist:
                a.head.d = dist
                a.head.predecessor = a.tail
                opt_cond = False
                n = a.head
        if dist < min_dist:
            opt_cond = True
            g.nCycle = n
    g.exec_time = timer() - start_time
    return g


