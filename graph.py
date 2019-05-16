import math
from typing import List


class Node:

    def __init__(self, v: int):
        self.value: int = v
        self.d = math.inf
        self.inList: List[Arc] = []
        self.outList: List[Arc] = []
        self.pre = None
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
    nodeList: List[Node] = []
    arcList: List[Arc] = []
    s: Node = None
    t: Node = None

    def number(self):
        i=1
        for n in self.nodeList:
            n.num=i
            i+=1
