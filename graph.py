import math
from typing import List


class Node:

    def __init__(self, v: int):
        self.value: int = v
        self.d = math.inf
        self.inList: List[Arc] = []
        self.outList: List[Arc] = []
        self.predecessor = None
        self.pred_arc = None
        self.num: int = None
        self.labeled = False
        self.contained = False
        self.previously = False
        self.in_degree = 0
        self.order = 0

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


class Graph:

    def __init__(self):
        self.node_list: List[Node] = []
        self.arc_list: List[Arc] = []
        self.ordered: List[Node] = []
        self.s: Node = None
        self.t: Node = None
        self.negative = False
        self.C = -math.inf
        self.nodes_number = 0
        self.exec_time = 0.0
        self.is_ordered = False

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
        self.s.d = 0
        self.order()

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
        new_list = []
        for n in self.node_list:
            if n.in_degree == 0:
                new_list.append(n)
        while len(new_list) > 0:
            n = new_list.pop(0)
            next_n += 1
            n.order = next_n
            self.ordered.append(n)
            for a in n.outList:
                a.head.in_degree -= 1
                if a.head.in_degree == 0:
                    new_list.append(a.head)
        self.is_ordered = next_n >= len(self.node_list)

    def set_residual(self):
        for a in self.arc_list:
            a.residual_forward_capacity = a.capacity - a.flow
            a.residual_reverse_capacity = a.flow
