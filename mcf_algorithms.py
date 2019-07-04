from timeit import default_timer as timer
from max_flow_algorithms import labeling
from spp_algorithms import fifo_label_correcting
from copy import deepcopy as dcp
from graph import *


def get_graph_for_feasible_solution(g: Graph):
    fg = dcp(g)
    b = 0
    neg = 0
    for n in fg.node_list:
        b += n.value
        if n.value < 0:
            neg += n.value
    if b != 0:
        return None
    s = Node(-neg)
    t = Node(neg)
    for n in fg.node_list:
        if n.value > 0:
            a = Arc(s, n, 0, n.value)
            s.outList.append(a)
            n.inList.append(a)
            fg.arc_list.append(a)
        elif n.value < 0:
            a = Arc(n, t, 0, -n.value)
            n.outList.append(a)
            t.inList.append(a)
            fg.arc_list.append(a)
    fg.node_list.insert(0, s)
    fg.node_list.append(t)
    fg.number()
    fg.s = s
    fg.t = t
    return fg


def is_feasible(fg: Graph):
    for a in fg.s.outList:
        if a.capacity - a.flow != 0:
            return False
    for a in fg.t.inList:
        if a.capacity - a.flow != 0:
            return False
    return True


def modified_deque_label_correcting(g: Graph):
    g.initialize()
    min_dist = -g.nodes_number * g.C
    n_cycle = g.t
    q = [g.s]
    g.s.contained = True

    while len(q) > 0:
        n = q.pop(0)
        n.contained = False
        for a in n.outList:
            dist = a.tail.d + a.cost
            if a.head.d > dist and a.residual_forward_capacity > 0:
                a.head.d = dist
                a.head.predecessor = a.tail
                a.head.pred_arc = a
                if not a.head.contained:
                    if a.head.previously:
                        q.insert(0, a.head)
                    else:
                        q.append(a.head)
                    a.head.contained = True
                    a.head.previously = True

        for a in n.inList:
            dist = a.head.d - a.cost
            if a.tail.d > dist and a.residual_reverse_capacity > 0:
                a.tail.d = dist
                a.tail.predecessor = a.head
                a.tail.pred_arc = a
                if not a.tail.contained:
                    if a.tail.previously:
                        q.insert(0, a.tail)
                    else:
                        q.append(a.tail)
                    a.tail.contained = True
                    a.tail.previously = True

        if dist < min_dist:
            n_cycle = n
            q.clear()
            g.neg_cycle = True
            return n_cycle

    g.neg_cycle = False
    return n_cycle


def new_path_search(fgraph: Graph):
    n_cycle = modified_deque_label_correcting(fgraph)
    n: Node = n_cycle
    if n != fgraph.t:
        return True
    arcs = []
    min_res_cap = math.inf
    fgraph.previously()
    path = Path()
    fgraph.paths.append(path)
    while n.predecessor is not None and not n.previously:
        arcs.append(n.pred_arc)

        path.node_list.append(n)
        if n.pred_arc.head == n:
            if min_res_cap > n.pred_arc.residual_forward_capacity:
                min_res_cap = n.pred_arc.residual_forward_capacity

        elif n.pred_arc.tail == n:
            if min_res_cap > n.pred_arc.residual_reverse_capacity:
                min_res_cap = n.pred_arc.residual_reverse_capacity

        n.previously = True
        n = n.predecessor
        if n.previously:
            fgraph.neg_cycle = True
            path.node_list.append(n)
            path.node_list.pop(0)
            return True
    n = n_cycle

    for a in arcs:
        if n.pred_arc.head == n:
            a.set_flow(a.flow + min_res_cap)
        else:
            a.set_flow(a.flow - min_res_cap)
        n = n.predecessor
    fgraph.source_flow -= min_res_cap
    path.flow = min_res_cap
    path.node_list.pop(0)

    return False


def successive_shortest_path(g: Graph):
    test_for_neg_cycle = fifo_label_correcting(dcp(g))
    if test_for_neg_cycle.neg_cycle:
        return test_for_neg_cycle
    g.reset_flows()
    g.paths.clear()
    times = 0
    fgraph = get_graph_for_feasible_solution(g)
    if fgraph is None:
        g.mcf_error = True
        return g
    fgraph = labeling(fgraph)
    if not is_feasible(fgraph):
        g.not_feasible = True
        return g
    fgraph.reset_flows()
    fgraph.set_source_residual_flow()
    flow = fgraph.source_flow
    neg_cycle_present = False
    start_time = timer()
    while flow > 0 and not neg_cycle_present:
        times += 1
        neg_cycle_present = new_path_search(fgraph)
        flow = fgraph.source_flow
    g.exec_time = timer() - start_time
    g.times = times
    g.paths.clear()
    g.paths = [p for p in fgraph.paths]
    g.node_list = fgraph.node_list
    g.arc_list = [a for a in fgraph.arc_list]
    for a in g.node_list[0].outList:
        g.arc_list.remove(a)
        a.head.inList.remove(a)
    for a in g.node_list[-1].inList:
        g.arc_list.remove(a)
        a.tail.outList.remove(a)
    g.node_list.pop(0)
    g.node_list.pop(-1)
    g.number()
    g.neg_cycle = fgraph.neg_cycle
    return g


def flow_neg_cycle(n, g):
    min_res_cap = math.inf
    g.previously()
    path = Path()
    path.cycle = True
    g.paths.append(path)
    while n.previously is not True:
        n.previously = True
        n = n.predecessor
    g.previously()
    while n.previously is not True:
        path.arc_list.append(n.pred_arc)
        path.node_list.append(n)
        n.previously = True
        n = n.predecessor
    path.node_list.append(n)
    node = 0
    path.node_list.reverse()
    path.arc_list.reverse()
    for a in path.arc_list:
        n = path.node_list[node]
        node += 1
        if a.tail == n:
            if min_res_cap > a.residual_forward_capacity:
                min_res_cap = a.residual_forward_capacity
        else:
            if min_res_cap > a.residual_reverse_capacity:
                min_res_cap = a.residual_reverse_capacity
    node = 0
    for a in path.arc_list:
        n = path.node_list[node]
        node += 1
        if a.tail == n:
            a.set_flow(a.flow + min_res_cap)
        else:
            a.set_flow(a.flow - min_res_cap)
    path.flow = min_res_cap


def cycle_canceling(g: Graph):
    test_for_neg_cycle = fifo_label_correcting(dcp(g))
    if test_for_neg_cycle.neg_cycle:
        return test_for_neg_cycle
    g.reset_flows()
    g.paths.clear()
    times = 0
    f_graph = get_graph_for_feasible_solution(g)
    if f_graph is None:
        g.mcf_error = True
        return g
    f_graph = labeling(f_graph)
    if not is_feasible(f_graph):
        g.not_feasible = True
        return g
    g = f_graph
    for a in g.node_list[0].outList:
        g.arc_list.remove(a)
        a.head.inList.remove(a)
    for a in g.node_list[-1].inList:
        g.arc_list.remove(a)
        a.tail.outList.remove(a)
    g.node_list.pop(0)
    g.node_list.pop(-1)
    g.number()
    g.s = g.node_list[0]
    g.t = g.node_list[-1]
    g.neg_cycle = True
    start_time = timer()
    while g.neg_cycle:
        n = modified_deque_label_correcting(g)
        if g.neg_cycle:
            flow_neg_cycle(n, g)
            times += 1
    g.exec_time = timer() - start_time
    g.times = times
    return g
