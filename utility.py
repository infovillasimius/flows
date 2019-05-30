from graph import *


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
                    my_graph.arc_list.append(Arc(cost=cost[row][col], capacity=cap[row][col], tail=my_graph.node_list[row],
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


def print_result(g, algo):
    n = g.t
    cost = n.d
    path = []
    while n != g.s:
        path.append(n)
        n = n.predecessor
    path.append(n)
    path.reverse()
    result = algo + " Algorithm\nSolution nodes = " + str(path) + "\n" + "Total cost = " + str(cost) + "\n"
    return result


def print_result2(g, algo):
    max_flow_s = 0
    max_flow_t = 0
    for a in g.s.outList:
        max_flow_s += a.flow
    for a in g.t.inList:
        max_flow_t += a.flow
    result = algo + " Algorithm\nFlow exiting the source = " + str(max_flow_s) + "\n" + "Flow entering the sink = " + str(max_flow_t) + "\n"
    return result
