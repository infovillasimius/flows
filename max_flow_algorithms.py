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
