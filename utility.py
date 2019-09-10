from graph import *
from copy import deepcopy as dcp


# Load Graph from a file
from spp_algorithms import fifo_label_correcting


def file_load(file):
    my_graph = Graph()
    try:
        stream = open(file, "rt")
        numbers = []

        lines = stream.readlines()
        for l in lines:
            for s in l.split():
                numbers.append(int(s))
        stream.close()
        n = numbers.pop(0)

        if n < 2:
            return None

        val = [numbers.pop(0) for x in range(n)]
        nad = [[numbers.pop(0) for x in range(n)] for y in range(n)]
        cost = [[numbers.pop(0) for x in range(n)] for y in range(n)]
        cap = [[numbers.pop(0) for x in range(n)] for y in range(n)]

        for i in range(n):
            my_graph.node_list.append(Node(val[i]))

        for row in range(n):
            for col in range(n):
                if nad[row][col] == 1:
                    my_graph.arc_list.append(
                        Arc(cost=cost[row][col], capacity=cap[row][col], tail=my_graph.node_list[row],
                            head=my_graph.node_list[col]))

        for a in my_graph.arc_list:
            a.head.inList.append(a)
            a.tail.outList.append(a)

        my_graph.s = my_graph.node_list[0]
        my_graph.t = my_graph.node_list[-1]

        my_graph.number()
        my_graph.negative_cost_detector()

    except Exception as exc:
        print("Error in loading graph:", exc)

    return my_graph


# Return negative cycle found by label correcting algorithms
def print_neg_cycle(g: Graph):
    g.previously()
    path = Path()
    path.cycle = True
    n = g.nCycle
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
    path.node_list.reverse()
    path.arc_list.reverse()
    path.cost = 0
    for arc in path.arc_list:
        path.cost += arc.cost
    return path


# Return results for Shortest Path Algorithms
def print_result(g: Graph, algorithm):
    result = algorithm + " Algorithm\n"
    if g is None:
        return result + "No result"
    if g.neg_cycle:
        path = print_neg_cycle(g)
        result = result + "Negative Cycle detected!\n" + str(path.node_list) + ": Total cost = " + str(path.cost) + '\n'
        return result
    n = g.t
    cost = n.d
    path = []
    while n != g.s:
        path.append(n)
        n = n.predecessor
    path.append(n)
    path.reverse()
    result = result + "Solution nodes = " + str(path) + "\n" + "Total cost = " + str(cost) + "\n"
    return result


# Return results for Shortest Path Neg Check Algorithms
def neg_check_print_result(g: Graph, algorithm):
    result = algorithm + " Algorithm\n"
    if g is None:
        return result + "No result"
    if g.neg_cycle:
        g1 = fifo_label_correcting(dcp(g))
        path = print_neg_cycle(g1)
        result = result + "Negative Cycle detected!\n" + str(path.node_list) + ": Total cost = " + str(path.cost) + '\n\n'

    n = g.t
    cost = n.d
    path = []
    while n != g.s:
        path.append(n)
        n = n.predecessor
    path.append(n)
    path.reverse()
    result = result + "Solution nodes = " + str(path) + "\n" + "Total cost = " + str(cost) + "\n"
    return result


# Return results for Max Flow Algorithms
def print_result2(g, algorithm_name):
    if g is None:
        return algorithm_name + " Algorithm\nNo result"
    max_flow_s = 0
    max_flow_t = 0
    for a in g.s.outList:
        max_flow_s += a.flow
    for a in g.t.inList:
        max_flow_t += a.flow
    result = algorithm_name + " Algorithm\nFlow exiting the source = " + str(
        max_flow_s) + "\n" + "Flow entering the sink = " + str(max_flow_t) + "\n"
    return result


# Return results for Successive Shortest Path Algorithm
def print_result3(g: Graph, algorithm_name):
    result = algorithm_name + " Algorithm\n"
    if g is None:
        return result + "\nNo result"
    if g.neg_cycle:
        path = print_neg_cycle(g)
        result = result + "Negative Cycle detected!\n" + str(path.node_list) + ": Total cost = " + str(path.cost)
        return result

    result += "\nNode Mass Balances b(i): " + str([a.value for a in g.node_list])
    result += "\nSuccessive paths: " + str(g.times) + "\nTotal cost: " + str(
        g.get_cost()) + "\nFlows Paths: " + str([(a.node_list[::-1], a.flow) for a in g.paths]) + "\n"
    return result


# Return results for Flow Decomposition Algorithm
def print_result4(paths, cycles):
    result = "\nFlow Decomposition Algorithm\nFlows Paths: " + str(
        [(a.node_list, a.flow) for a in paths]) + "\nFlow Cycles: " + str(
        [(a.node_list, a.flow) for a in cycles])
    return result


# Return results for Cycle canceling Algorithm
def print_result5(g: Graph, algorithm_name):
    result = algorithm_name + " Algorithm\n"
    if g is None:
        return result + "\nNo result"
    if g.neg_cycle:
        path = print_neg_cycle(g)
        result = result + "Negative Cycle detected!\n" + str(path.node_list) + ": Total cost = " + str(path.cost)
        return result

    result += "\nNode Mass Balances b(i): " + str([a.value for a in g.node_list])
    result += "\nNumber of Cycles : " + str(g.times) + "\nTotal cost: " + str(
        g.get_cost()) + "\nCanceled Cycles: " + str([(a.node_list, a.flow) for a in g.paths]) + "\n"
    return result


# Return initial node for "Flow Decomposition" Algorithm
def get_initial_node(g: Graph):
    for n in g.node_list:
        in_flow = 0
        out_flow = 0
        for a in n.inList:
            in_flow += a.flow
        for a in n.outList:
            out_flow += a.flow
        if in_flow < out_flow:
            n.flow_balance = out_flow - in_flow
            return n
    return None


# Depth First Search for "Flow Decomposition" Algorithm
def depth_first_search(n: Node, g: Graph):
    g.previously()
    q = [n]
    n.previously = True
    excess_node_list = []
    path = Path()
    path.flow = n.flow_balance
    path.node_list.append(n)

    for node in g.node_list:
        in_flow = 0
        out_flow = 0
        for a in node.inList:
            in_flow += a.flow
        for a in node.outList:
            out_flow += a.flow
        if in_flow > out_flow:
            node.flow_balance = in_flow - out_flow
            excess_node_list.append(node)

    while len(q) > 0:
        node = q[-1]
        not_found = True
        for a in node.outList:
            if a.head == n and a.flow > 0:
                path.flow = min(path.flow, a.flow)
                path.node_list.append(a.head)
                path.cycle = True
                return path
            elif excess_node_list.__contains__(a.head) and a.flow > 0:
                path.flow = min(path.flow, a.flow, a.head.flow_balance)
                path.node_list.append(a.head)
                path.arc_list.append(a)
                return path
            if not a.head.previously and a.flow > 0:
                path.flow = min(path.flow, a.flow)
                a.head.previously = True
                q.append(a.head)
                not_found = False
                path.node_list.append(a.head)
                path.arc_list.append(a)
                break
        if not_found:
            q.pop(-1)

    return None


# Flow Decomposition Algorithm
def flow_decomposition(g: Graph):
    path_list = []
    cycle_list = []
    n = get_initial_node(g)
    while n is not None:
        w = depth_first_search(n, g)
        for a in w.arc_list:
            a.flow -= w.flow
        if w.cycle:
            cycle_list.append(w)
        else:
            path_list.append(w)
        n = get_initial_node(g)
    return path_list, cycle_list


# Execute statistic tests on the algorithm passed as argument
def test(tests: int, g: Graph, algorithm):
    best = math.inf
    mean = 0

    if tests < 1:
        tests = 1
    for x in range(tests):
        gg = algorithm(dcp(g))
        best = min(gg.exec_time, best)
        mean += gg.exec_time
    mean *= 1000 / tests
    result = "Time statistics on " + str(tests) + " execution"
    if tests > 1:
        result = result + "s"
    result = result + "\nBest time (milliseconds)= " + str(
        best * 1000) + "\n" + "Mean (milliseconds)= " + str(mean) + "\n"
    return result
