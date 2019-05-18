import tkinter as tk
from copy import deepcopy as dcp
from tkinter import filedialog
import time
from graph import *
from spp_algorithms import *


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

        my_graph.s = my_graph.nodeList[0]
        my_graph.t = my_graph.nodeList[-1]

        my_graph.number()
        my_graph.negative_cost_detector()

    except Exception as exc:
        print("Error in loading graph:", exc)

    return my_graph


def print_result(g):
    if g.negative:
        result="Negative arc cost detected!\n"
        return result

    n = g.t
    cost = n.d
    path = []
    while n != g.s:
        path.append(n)
        n = n.predecessor
    path.append(n)
    path.reverse()
    result="Dijkstra Algorithm\nExecution time (seconds) = "+str(g.exec_time)+"\n"+"Solution nodes = "+str(path)+"\n"+"Total cost = "+str(cost)+"\n"
    return result


class App(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.graph = None
        self.min_x = 300
        self.min_y = 200
        self.max_x = 600
        self.max_y = 200
        self.create_widgets()

    def create_widgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(1, weight=1)
        top.columnconfigure(0, weight=1)
        top.minsize(self.min_x, self.min_y)
        top.maxsize(self.max_x, self.max_y)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
        self.dijkstraButton = tk.Button(self, text='Dijkstra', command=self.execDijkstra)
        self.dijkstraButton.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        self.loadButton = tk.Button(self, text='Load a graph from file', command=self.load)
        self.loadButton.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.resultText = tk.Text(self)   #, width=40, height=10)
        self.resultText.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W, columnspan=3)

    def execDijkstra(self):
        if self.graph is not None:
            g = dijkstra(dcp(self.graph))
            result=print_result(g)
            self.resultText.delete('1.0',tk.END)
            self.resultText.insert(tk.INSERT,result)
        else:
            print("Graph not loaded")

    def load(self):
        p = tk.Tk
        p.filename = filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(("text files", "*.txt"),
                                                                                                ("all files", "*.*")))
        if len(p.filename) > 0:
            self.graph = file_load(p.filename)
            self.resultText.insert(tk.INSERT, "Graph loaded!")
        else:
            self.resultText.insert(tk.INSERT, "Error loading graph!")


app = App()
app.master.title('Network Flows Optimization')
app.mainloop()
