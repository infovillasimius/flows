from timeit import default_timer as timer
from max_flow_algorithms import labeling
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
    nCycle = g.t
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
            nCycle = n
            q.clear()
            g.neg_cycle = True
            return nCycle

    g.neg_cycle = False
    return nCycle


def new_path_search(fgraph: Graph):
    ncycle = modified_deque_label_correcting(fgraph)
    n: Node = ncycle
    if n != fgraph.t:
        print("Error")
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
    n = ncycle

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
    for a in g.node_list[-1].inList:
        g.arc_list.remove(a)
    g.node_list.pop(0)
    g.node_list.pop(-1)
    g.number()
    return g
