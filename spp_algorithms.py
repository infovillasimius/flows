from timeit import default_timer as timer
from queues import *
from graph import *


def dynamic(g):
    g.initialize()
    if not g.is_ordered:
        return g
    start_time = timer()
    for n in g.node_list:
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
    my_list = g.node_list
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
    my_list = g.node_list
    g.initialize()
    q = CircularQueue(g.C + 1)
    q.store(g.s)
    start_time = timer()
    while len(my_list) > 0:
        n = q.next()
        if not n.labeled:
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
    my_list = g.node_list
    g.initialize()
    q = RadixHeap(g.nodes_number * g.C)
    q.store(g.s)
    g.s.labeled = True
    start_time = timer()
    while len(my_list) > 0:
        n = q.next()
        n.labeled = False
        my_list.remove(n)
        for a in n.outList:
            dist = a.tail.d + a.cost
            old_d = a.head.d
            if old_d > dist:
                a.head.d = dist
                a.head.predecessor = a.tail
                if a.head.labeled:
                    q.update(node=a.head, old_d=old_d)
                else:
                    a.head.labeled = True
                    q.store(a.head)
    g.exec_time = timer() - start_time
    return g


def label_correcting(g: Graph):
    g.initialize()
    min_dist = -g.nodes_number * g.C
    opt_cond = False
    start_time = timer()

    while not opt_cond:
        opt_cond = True
        for a in g.arc_list:
            dist = a.tail.d + a.cost
            if a.head.d > dist:
                a.head.d = dist
                a.head.predecessor = a.tail
                opt_cond = False
                n = a.head
        if dist < min_dist:
            opt_cond = True
            g.nCycle = n
            g.neg_cycle = True

    g.exec_time = timer() - start_time
    return g


def fifo_label_correcting(g):
    g.initialize()
    min_dist = -g.nodes_number * g.C
    g.nCycle = None
    q = [g.s]
    g.s.contained = True
    start_time = timer()

    while len(q) > 0:
        n = q.pop(0)
        n.contained = False
        for a in n.outList:
            dist = a.tail.d + a.cost
            if a.head.d > dist:
                a.head.d = dist
                a.head.predecessor = a.tail
                if not a.head.contained:
                    q.append(a.head)
                    a.head.contained = True
        if dist < min_dist:
            g.nCycle = n
            g.neg_cycle = True
            q.clear()

    g.exec_time = timer() - start_time
    return g


def deque_label_correcting(g):
    g.initialize()
    min_dist = -g.nodes_number * g.C
    g.nCycle = None
    q = [g.s]
    g.s.contained = True
    start_time = timer()

    while len(q) > 0:
        n = q.pop(0)
        n.contained = False
        for a in n.outList:
            dist = a.tail.d + a.cost
            if a.head.d > dist:
                a.head.d = dist
                a.head.predecessor = a.tail
                if not a.head.contained:
                    if a.head.previously:
                        q.insert(0,a.head)
                    else:
                        q.append(a.head)
                    a.head.contained = True
                    a.head.previously = True
        if dist < min_dist:
            g.nCycle = n
            g.neg_cycle = True
            q.clear()

    g.exec_time = timer() - start_time
    return g


