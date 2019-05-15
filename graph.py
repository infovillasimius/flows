import math
from typing import List


class Node:

    def __init__(self, v: int):
        self.value: int = v
        self.d = math.inf
        self.inList: List[Arc] = []
        self.outList: List[Arc] = []
        self.pre = None


class Arc:

    def __init__(self, tail: Node, head: Node, cost: int = 0):
        self.cost = cost
        self.capacity = math.inf
        self.head = head
        self.tail = tail


class Graph:
    nodeList: List[Node] = []
    arcList: List[Arc] = []
    s: Node = None
    t: Node = None
