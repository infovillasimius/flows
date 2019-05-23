import tkinter as tk
from copy import deepcopy as dcp
from tkinter import filedialog
from spp_algorithms import *
from utility import *


class App(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.graph = None
        self.min_x = 400
        self.min_y = 200
        self.max_x = 800
        self.max_y = 400
        self.create_widgets()

    def create_widgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        top.minsize(self.min_x, self.min_y)
        top.maxsize(self.max_x, self.max_y)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.loadButton = tk.Button(self, text='Load a graph from file', command=self.load)
        self.loadButton.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.dijkstraButton = tk.Button(self, text='Dynamic', command=self.exec_dynamic)
        self.dijkstraButton.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        self.dijkstraButton = tk.Button(self, text='Dijkstra', command=self.exec_dijkstra)
        self.dijkstraButton.grid(row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
        self.dial_dijkstraButton = tk.Button(self, text='Dial Dijkstra', command=self.exec_dial_dijkstra)
        self.dial_dijkstraButton.grid(row=0, column=3, sticky=tk.N + tk.S + tk.E + tk.W)
        self.radix_heap_dijkstraButton = tk.Button(self, text='Radix Heap Dijkstra', command=self.exec_radix_heap_dijkstra)
        self.radix_heap_dijkstraButton.grid(row=0, column=4, sticky=tk.N + tk.S + tk.E + tk.W)
        self.label_correctingButton = tk.Button(self, text='Label Correcting', command=self.exec_label_correcting)
        self.label_correctingButton.grid(row=0, column=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=0, column=6, sticky=tk.N + tk.S + tk.E + tk.W)
        self.resultText = tk.Text(self)  # , width=40, height=10)
        self.resultText.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W, columnspan=7)
        self.entry_label=tk.Label(self, text='Number of test cycles')
        self.entry_label.grid(row=3, column=0)
        self.entry=tk.Entry(self, justify=tk.CENTER)

        self.entry.insert(0,'1')
        self.entry.grid(row=3, column=1)

    def load(self):
        self.resultText.delete('1.0', tk.END)
        p = tk.Tk
        p.filename = filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(("text files", "*.txt"),
                                                                                                ("all files", "*.*")))
        if len(p.filename) > 0:
            self.graph = file_load(p.filename)
            self.resultText.insert(tk.INSERT, "Graph loaded!")
        else:
            self.resultText.insert(tk.INSERT, "Error loading graph!")

    def exec_dynamic(self):
        self.resultText.delete('1.0', tk.END)
        if self.graph is not None:
            g = dynamic(dcp(self.graph))
            if not g.is_ordered:
                result = "Cycle detected!\n"
            else:
                result = print_result(g, "Dynamic")
                best = math.inf
                mean = 0
                tests = int(self.entry.get())
                if tests < 1:
                    tests = 1
                for x in range(tests):
                    gg = dynamic(dcp(self.graph))
                    best = min(gg.exec_time, best)
                    mean += gg.exec_time
                mean *= 1000 / tests
                result = result + "Time statistics on " + str(tests) + " execution"
                if tests > 1:
                    result = result + "s"
                result = result + "\nBest time (milliseconds)= " + str(
                    best * 1000) + "\n" + "Mean (milliseconds)= " + str(mean) + "\n"
            self.resultText.insert(tk.INSERT, result)
        else:
            self.resultText.insert(tk.INSERT, "Graph not loaded")

    def exec_dijkstra(self):
        self.resultText.delete('1.0', tk.END)
        if self.graph is not None:
            g = dijkstra(dcp(self.graph))
            if g.negative:
                result = "Negative arc cost detected!\n"
            else:
                result = print_result(g, "Dijkstra")
                best = math.inf
                mean = 0
                tests = int(self.entry.get())
                if tests < 1:
                    tests = 1
                for x in range(tests):
                    gg = dijkstra(dcp(self.graph))
                    best = min(gg.exec_time, best)
                    mean += gg.exec_time
                mean *= 1000 / tests
                result = result + "Time statistics on " + str(tests) + " execution"
                if tests > 1:
                    result = result + "s"
                result = result + "\nBest time (milliseconds)= " + str(
                    best * 1000) + "\n" + "Mean (milliseconds)= " + str(mean) + "\n"
            self.resultText.insert(tk.INSERT, result)
        else:
            self.resultText.insert(tk.INSERT, "Graph not loaded")

    def exec_dial_dijkstra(self):
        self.resultText.delete('1.0', tk.END)
        if self.graph is not None:
            g = dial_dijkstra(dcp(self.graph))
            if g.negative:
                result = "Negative arc cost detected!\n"
            else:
                result = print_result(g, "Dial Dijkstra")
                best = math.inf
                mean = 0
                tests = int(self.entry.get())
                if tests < 1:
                    tests = 1
                for x in range(tests):
                    gg = dial_dijkstra(dcp(self.graph))
                    best = min(gg.exec_time, best)
                    mean += gg.exec_time
                mean *= 1000 / tests
                result = result + "Time statistics on " + str(tests) + " execution"
                if tests > 1:
                    result = result + "s"
                result = result + "\nBest time (milliseconds)= " + str(
                    best * 1000) + "\n" + "Mean (milliseconds)= " + str(mean) + "\n"
            self.resultText.insert(tk.INSERT, result)
        else:
            self.resultText.insert(tk.INSERT, "Graph not loaded")

    def exec_radix_heap_dijkstra(self):
        self.resultText.delete('1.0', tk.END)
        if self.graph is not None:
            g = radix_heap_dijkstra(dcp(self.graph))
            if g.negative:
                result = "Negative arc cost detected!\n"
            else:
                result = print_result(g, "Radix Heap Dijkstra")
                best = math.inf
                mean = 0
                tests = int(self.entry.get())
                if tests < 1:
                    tests = 1
                for x in range(tests):
                    gg = radix_heap_dijkstra(dcp(self.graph))
                    best = min(gg.exec_time, best)
                    mean += gg.exec_time
                mean *= 1000/tests
                result = result + "Time statistics on "+str(tests)+" execution"
                if tests > 1:
                    result = result + "s"
                result = result+"\nBest time (milliseconds)= "+ str(best*1000) + "\n" + "Mean (milliseconds)= " + str(mean) + "\n"
            self.resultText.insert(tk.INSERT, result)
        else:
            self.resultText.insert(tk.INSERT, "Graph not loaded")

    def exec_label_correcting(self):
        self.resultText.delete('1.0', tk.END)
        if self.graph is not None:
            g = label_correcting(dcp(self.graph))
            result = print_result(g, "Label Correcting")
            best = math.inf
            mean = 0
            tests = int(self.entry.get())
            if tests < 1:
                tests = 1
            for x in range(tests):
                gg = label_correcting(dcp(self.graph))
                best = min(gg.exec_time, best)
                mean += gg.exec_time
            mean *= 1000 / tests
            result = result + "Time statistics on " + str(tests) + " execution"
            if tests > 1:
                result = result + "s"
            result = result + "\nBest time (milliseconds)= " + str(best * 1000) + "\n" + "Mean (milliseconds)= " + str(
                mean) + "\n"
            self.resultText.insert(tk.INSERT, result)
        else:
            self.resultText.insert(tk.INSERT, "Graph not loaded")


app = App()
app.master.title('Network Flows Optimization')
app.mainloop()
