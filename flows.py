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
        self.dijkstraButton = tk.Button(self, text='Dijkstra', command=self.exec_dijkstra)
        self.dijkstraButton.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        self.dial_dijkstraButton = tk.Button(self, text='Dial Dijkstra', command=self.exec_dial_dijkstra)
        self.dial_dijkstraButton.grid(row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
        self.label_correctingButton = tk.Button(self, text='Label Correcting', command=self.exec_label_correcting)
        self.label_correctingButton.grid(row=0, column=3, sticky=tk.N + tk.S + tk.E + tk.W)
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=0, column=4, sticky=tk.N + tk.S + tk.E + tk.W)
        self.resultText = tk.Text(self)  # , width=40, height=10)
        self.resultText.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W, columnspan=5)

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

    def exec_dijkstra(self):
        self.resultText.delete('1.0', tk.END)
        if self.graph is not None:
            g = dijkstra(dcp(self.graph))
            if g.negative:
                result = "Negative arc cost detected!\n"
            else:
                result = print_result(g, "Dijkstra")
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
            self.resultText.insert(tk.INSERT, result)
        else:
            self.resultText.insert(tk.INSERT, "Graph not loaded")

    def exec_label_correcting(self):
        self.resultText.delete('1.0', tk.END)
        if self.graph is not None:
            g = label_correcting(dcp(self.graph))
            result = print_result(g, "Label Correcting")
            self.resultText.insert(tk.INSERT, result)
        else:
            self.resultText.insert(tk.INSERT, "Graph not loaded")


app = App()
app.master.title('Network Flows Optimization')
app.mainloop()
