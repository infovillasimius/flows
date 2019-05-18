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
        return self.tail.__str__()+" -> "+self.head.__str__()

    def __repr__(self):
        return self.tail.__str__() + " -> " + self.head.__str__()


class Graph:

    def __init__(self):
        self.nodeList: List[Node] = []
        self.arcList: List[Arc] = []
        self.s: Node = None
        self.t: Node = None
        self.negative = False
        self.C=-math.inf
        self.nodes_number=0

    def number(self):
        i=1
        for n in self.nodeList:
            n.num=i
            i+=1

    def initialize(self):
        for n in self.nodeList:
            n.d = math.inf
        self.s.d = 0

    def negative_cost_detector(self):
        self.nodes_number = len(self.nodeList)
        print(self.nodes_number)
        for a in self.arcList:
            self.C=max(self.C,a.cost)
            if a.cost < 0:
                self.negative=True