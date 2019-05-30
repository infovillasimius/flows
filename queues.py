# queues definitions
import math


class CircularQueue:

    def __init__(self, n):
        self.__nodes = [None for x in range(n)]
        self.__n = n
        self.__size = 0
        self.__pointer = 0

    def store(self, node):
        if self.__nodes[node.d % self.__n] is None:
            self.__nodes[node.d % self.__n] = [node]
        else:
            self.__nodes[node.d % self.__n].append(node)
        self.__size += 1

    def next(self):
        if self.__size < 1:
            return None
        while self.__nodes[self.__pointer] is None:
            self.__pointer = (self.__pointer + 1) % self.__n
        self.__size -= 1
        node = self.__nodes[self.__pointer].pop(0)
        if len(self.__nodes[self.__pointer]) == 0:
            self.__nodes[self.__pointer] = None
        return node


class RadixHeap:

    def __init__(self, n):
        self.__base = 0
        if n <= 0:
            n = 8
        self.__b = math.ceil(math.log2(n))
        self.__w = [0 for x in range(self.__b)]
        self.__min = [0 for x in range(self.__b)]
        self.__width = [0 for x in range(self.__b)]
        self.__range = [0 for x in range(self.__b)]
        self.__h = [None for x in range(self.__b)]
        self.__pointer = 0
        self.__w[0] = 1
        self.__w[1] = 1
        self.__width[0] = 1
        self.__width[1] = 1
        self.__range[0] = 1
        self.__range[1] = 1
        for i in range(2, self.__b):
            self.__w[i] = self.__w[i - 1] * 2
            self.__width[i] = self.__w[i]
            self.__range[i] = self.__w[i]

    def __get_index(self, d):
        distance = d - self.__base
        if distance <= 0:
            return 0
        bucket = math.ceil(math.log2(distance))
        if (d >= self.__range[bucket]) and (d < self.__range[bucket] + self.__w[bucket]) and self.__w[bucket] > 0:
            return bucket
        for i in range(bucket, self.__b):
            if d >= self.__range[i] and (d < self.__range[i] + self.__w[i]) and self.__w[i] > 0:
                return i
        return 0

    def store(self, node):
        bucket = self.__get_index(node.d)
        if self.__h[bucket] is None:
            self.__h[bucket] = [node]
            self.__min[bucket] = node.d
        else:
            self.__h[bucket].append(node)
            self.__min[bucket] = min(self.__min[bucket], node.d)

    def __redist(self):
        chain = self.__h[self.__pointer]
        self.__h[self.__pointer] = None
        self.__range[0] = self.__min[self.__pointer]
        self.__base = self.__range[0]
        self.__range[1] = self.__range[0] + 1
        for i in range(2, self.__pointer):
            self.__w[i] = self.__width[i]
            self.__range[i] = self.__range[i - 1] + self.__w[i - 1]
        self.__range[self.__pointer] += self.__w[self.__pointer]
        self.__w[self.__pointer] = 0
        self.__w[self.__pointer - 1] = self.__range[self.__pointer] - self.__range[self.__pointer - 1]
        self.__w[0] = 1
        self.__w[1] = 1
        while len(chain) > 0:
            self.store(chain.pop(0))
        self.__pointer = 0

    def next(self):
        while self.__h[self.__pointer] is None:
            self.__pointer = (self.__pointer + 1) % self.__b
        if len(self.__h[self.__pointer]) == 1:
            r = self.__h[self.__pointer].pop()
            self.__h[self.__pointer] = None
        elif self.__w[self.__pointer] < 2:
            r = self.__h[self.__pointer].pop()
        else:
            self.__redist()
            return self.next()
        return r

    def update(self, node, old_d):
        old_bucket = self.__get_index(old_d)
        new_bucket = self.__get_index(node.d)
        if old_bucket != new_bucket:
            if node in self.__h[old_bucket]:
                self.__h[old_bucket].remove(node)
                if len(self.__h[old_bucket]) == 0:
                    self.__h[old_bucket] = None
            self.store(node)
