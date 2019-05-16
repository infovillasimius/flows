import tkinter as tk
from tkinter import filedialog
from graph import *
from copy import deepcopy as dcp


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
            my_graph.nodeList.append(Node(val[i]))

        for row in range(n):
            for col in range(n):
                if nad[row][col] == 1:
                    my_graph.arcList.append(Arc(cost=cost[row][col], cap=cap[row][col], tail=my_graph.nodeList[row],
                                                head=my_graph.nodeList[col]))

        for a in my_graph.arcList:
            a.head.inList.append(a)
            a.tail.outList.append(a)

        my_graph.s=my_graph.nodeList[0]
        my_graph.t=my_graph.nodeList[-1]

        my_graph.number()

    except Exception as exc:
        print("Error in loading graph:", exc)

    return my_graph


def dijkstra(g):
    my_list = g.nodeList
    for n in my_list:
        n.d = math.inf
    s = g.s
    s.d = 0
    while my_list.__len__() > 0:
        minor = math.inf
        for i in my_list:
            if i.d < minor:
                n = i
                minor = i.d
        my_list.remove(n)
        for a in n.outList:
            dist = a.tail.d + a.cost
            if a.head.d > dist:
                a.head.d = dist
                a.head.predecessor = a.tail
    return g


def print_result(g):
    n=g.t
    cost=n.d
    path=[]
    while n != g.s:
        path.append(n)
        n=n.predecessor
    path.append(n)
    path.reverse()

    print("Solution nodes = ", path)
    print("Total cost = ",cost)
    pass


class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.create_widgets()

    def create_widgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)


app = App()
app.master.title('Network Flows Optimization')

app.filename = filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(("text files", "*.txt"),
                                                                                          ("all files", "*.*")))
if len(app.filename) > 0:
    graph = file_load(app.filename)
else:
    graph = Graph()

g = dijkstra(dcp(graph))
print_result(g)

# print(graph.arcList, graph.nodeList, sep="\n")

# app.mainloop()
