import math
from timeit import default_timer as timer


def augment(t):
    n = t
    min_r = t.pred_arc.residual_forward_capacity

    while n.predecessor is not None:
        a = n.pred_arc
        if n.predecessor == a.tail:
            r = a.residual_forward_capacity
        else:
            r = a.residual_reverse_capacity
        if min_r > r:
            min_r = r
        n = n.predecessor
    n = t
    while n.predecessor is not None:
        a = n.pred_arc
        if n.predecessor == a.tail:
            a.flow += min_r
            a.residual_forward_capacity -= min_r
            a.residual_reverse_capacity += min_r
        else:
            a.flow -= min_r
            a.residual_forward_capacity += min_r
            a.residual_reverse_capacity -= min_r
        n = n.predecessor


def labeling(g):
    g.set_residual()
    s = g.s
    t = g.t
    t.previously = True
    my_list = []

    start_time = timer()
    while t.previously:
        for n in g.node_list:
            n.previously = False
            n.predecessor = None
            n.pred_arc = None
        s.previously = True
        my_list.clear()
        my_list.append(s)
        while len(my_list) > 0 and not t.previously:
            i = my_list.pop(0)
            for a in i.outList:
                if a.residual_forward_capacity > 0 and not a.head.previously:
                    a.head.predecessor = i
                    a.head.pred_arc = a
                    a.head.previously = True
                    my_list.append(a.head)
            for a in i.inList:
                if a.residual_reverse_capacity > 0 and not a.tail.previously:
                    a.tail.predecessor = i
                    a.tail.pred_arc = a
                    a.tail.previously = True
                    my_list.append(a.tail)
            if t.previously:
                augment(t)
    g.exec_time = timer() - start_time
    return g


def pre_process(g):
    g.reset_flows()
    g.reverse_breadth_first_search()
    s = g.s
    for a in s.outList:
        a.set_flow(a.capacity)
        g.active_node_list.append(a.head)
    s.d = g.nodes_number


def push_relabel(i, g):
    s = g.s
    t = g.t
    d = math.inf
    in_size = len(i.inList)
    out_size = len(i.outList)
    while i.mass_balance > 0:
        while i.mass_balance > 0 and i.active_forward_arc < out_size:
            a = i.outList[i.active_forward_arc]
            if a.head.d < a.tail.d and a.residual_forward_capacity > 0 and a.head != s:
                a.set_flow(a.flow + min(a.residual_forward_capacity, i.mass_balance))
                if a.head.mass_balance > 0 and a.head != t:
                    g.active_node_list.append(a.head)
            else:
                i.active_forward_arc += 1
        if i.active_forward_arc >= out_size:
            i.active_forward_arc = 0
        if i.mass_balance <= 0:
            return
        while i.mass_balance > 0 and i.active_reverse_arc < in_size:
            a = i.inList[i.active_reverse_arc]
            if a.residual_reverse_capacity > 0 and a.tail.d < a.head.d:
                a.set_flow(a.flow - min(a.residual_reverse_capacity, i.mass_balance))
                if a.tail.mass_balance > 0:
                    g.active_node_list.append(a.tail)
            else:
                i.active_reverse_arc += 1
        if i.active_reverse_arc >= in_size:
            i.active_reverse_arc = 0
        if i.mass_balance <= 0:
            return
        counter = 0
        for aa in i.outList:
            if aa.residual_forward_capacity > 0 and d > aa.head.d and aa.head != s:
                d = aa.head.d
                i.active_forward_arc = counter
            counter +=1

        counter = 0
        for aa in i.inList:
            if aa.residual_reverse_capacity > 0 and d > aa.tail.d:
                d = aa.tail.d
                i.active_reverse_arc = counter
                i.active_forward_arc = out_size
        i.d = d + 1
        d = math.inf


def pre_flow_push(g):
    t = g.t
    g.active_node_list.clear()
    pre_process(g)
    start_time = timer()
    while len(g.active_node_list) > 0:
        n = g.active_node_list.pop(0)
        if n.mass_balance > 0 and n != t:
            push_relabel(n, g)
    g.exec_time = timer() - start_time
    return g
