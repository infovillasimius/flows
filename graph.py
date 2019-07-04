import math
from typing import List


class Node:

    def __init__(self, v: int):
        self.value: int = v
        self.d = math.inf
        self.inList: List[Arc] = []
        self.outList: List[Arc] = []
        self.predecessor: Node = None
        self.pred_arc: Arc = None
        self.num: int = None
        self.labeled = False
        self.contained = False
        self.previously = False
        self.in_degree = 0
        self.order = 0
        self.mass_balance = 0
        self.flow_balance = 0
        self.active_forward_arc = 0
        self.active_reverse_arc = 0

    def __str__(self):
        return self.num.__str__()

    def __repr__(self):
        return self.num.__str__()


class Arc:
    def __init__(self, tail: Node, head: Node, cost=0, capacity=math.inf, flow=0):
        self.cost = cost
        self.capacity = capacity
        self.flow = flow
        self.residual_forward_capacity = capacity - flow
        self.residual_reverse_capacity = flow
        self.head = head
        self.tail = tail

    def __str__(self):
        return self.tail.__str__() + " -> " + self.head.__str__()

    def __repr__(self):
        return self.tail.__str__() + " -> " + self.head.__str__()

    def set_flow(self, flow):
        if flow < 0:
            return
        if flow <= self.capacity:
            delta = flow - self.flow
            self.flow = flow
        else:
            delta = self.capacity - self.flow
            self.flow = self.capacity
        self.residual_forward_capacity = self.capacity - self.flow
        self.residual_reverse_capacity = self.flow
        self.tail.mass_balance -= delta
        self.head.mass_balance += delta


class Path:
    def __init__(self):
        self.node_list: List[Node] = []
        self.arc_list: List[Arc] = []
        self.reverse = False
        self.cycle = False
        self.flow = 0
        self.cost = 0


class Graph:
    def __init__(self):
        self.node_list: List[Node] = []
        self.arc_list: List[Arc] = []
        self.ordered: List[Node] = []
        self.active_node_list: List[Node] = []
        self.paths: List[Path] = []
        self.s: Node = None
        self.t: Node = None
        self.negative = False
        self.neg_cycle = False
        self.nCycle = self.t
        self.not_feasible = False
        self.mcf_error = False
        self.C = -math.inf
        self.nodes_number = 0
        self.exec_time = 0.0
        self.is_ordered = False
        self.source_flow = 0
        self.times = 0

    def number(self):
        i = 1
        for n in self.node_list:
            n.num = i
            i += 1

    def initialize(self):
        for n in self.node_list:
            n.d = math.inf
            n.labeled = False
            n.previously = False
            n.contained = False
            n.predecessor = None
            n.pred_arc = None
        self.s.d = 0
        self.nCycle = self.t
        self.neg_cycle = False
        self.order()

    def previously(self):
        for n in self.node_list:
            n.previously = False

    def contained(self):
        for n in self.node_list:
            n.contained = False

    def negative_cost_detector(self):
        self.nodes_number = len(self.node_list)
        for a in self.arc_list:
            self.C = max(self.C, a.cost)
            if a.cost < 0:
                self.negative = True

    def order(self):
        for n in self.node_list:
            n.in_degree = 0
            n.order = 0
        next_n = 0
        for a in self.arc_list:
            a.head.in_degree += 1
        zero_in_degree_list = []
        for n in self.node_list:
            if n.in_degree == 0:
                zero_in_degree_list.append(n)
        while len(zero_in_degree_list) > 0:
            n = zero_in_degree_list.pop(0)
            next_n += 1
            n.order = next_n
            self.ordered.append(n)
            for a in n.outList:
                a.head.in_degree -= 1
                if a.head.in_degree == 0:
                    zero_in_degree_list.append(a.head)
        self.is_ordered = next_n >= len(self.node_list)

    def set_residual(self):
        for a in self.arc_list:
            a.residual_forward_capacity = a.capacity - a.flow
            a.residual_reverse_capacity = a.flow

    def reset_flows(self):
        for n in self.node_list:
            n.mass_balance = 0
            n.active_forward_arc = 0
        for a in self.arc_list:
            a.flow = 0
        self.set_residual()

    def reverse_breadth_first_search(self):
        self.previously()
        q = [self.t]
        self.t.previously = True
        self.t.d = 0
        while len(q) > 0:
            n = q.pop(0)
            for a in n.inList:
                if not a.tail.previously:
                    a.tail.previously = True
                    a.tail.d = n.d + 1
                    q.append(a.tail)

    def set_source_residual_flow(self):
        self.source_flow = 0
        for a in self.s.outList:
            self.source_flow += a.residual_forward_capacity

    def get_cost(self):
        total_cost = 0
        for a in self.arc_list:
            total_cost += a.flow * a.cost
        return total_cost
