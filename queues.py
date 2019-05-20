# queues definitions


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
