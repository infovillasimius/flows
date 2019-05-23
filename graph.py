import math
from typing import List


class Node:

    def __init__(self, v: int):
        self.value: int = v
        self.d = math.inf
        self.inList: List[Arc] = []
        self.outList: List[Arc] = []
        self.predecessor = None
        self.num: int = None
        self.labeled = False
        self.in_degree = 0
        self.order = 0

    def __str__(self):
        return self.num.__str__()

    def __repr__(self):
        return self.num.__str__()


class Arc:

    def __init__(self, tail: Node, head: Node, cost: int = 0, cap=math.inf):
        self.cost = cost
        self.cap = cap
        self.head = head
        self.tail = tail

    def __str__(self):
        return self.tail.__str__() + " -> " + self.head.__str__()

    def __repr__(self):
        return self.tail.__str__() + " -> " + self.head.__str__()


class Graph:

    def __init__(self):
        self.nodeList: List[Node] = []
        self.arcList: List[Arc] = []
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
        for n in self.nodeList:
            n.num = i
            i += 1

    def initialize(self):
        for n in self.nodeList:
            n.d = math.inf
            n.labeled = False
        self.s.d = 0
        self.order()

    def negative_cost_detector(self):
        self.nodes_number = len(self.nodeList)

        for a in self.arcList:
            self.C = max(self.C, a.cost)
            if a.cost < 0:
                self.negative = True

    def order(self):
        for n in self.nodeList:
            n.in_degree = 0
            n.order = 0
            next_n = 0
        for a in self.arcList:
            a.head.in_degree += 1
        new_list = []
        for n in self.nodeList:
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
        self.is_ordered = next_n >= len(self.nodeList)
