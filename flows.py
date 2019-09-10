import tkinter as tk
from copy import deepcopy as dcp
from tkinter import filedialog

from mcf_algorithms import successive_shortest_path, cycle_canceling
from spp_algorithms import *
from max_flow_algorithms import *
from utility import *


class App(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.graph = None
        self.min_x = 400
        self.min_y = 400
        self.max_x = 1200
        self.max_y = 500
        self.create_widgets()

    def create_widgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        top.minsize(self.min_x, self.min_y)
        top.maxsize(self.max_x, self.max_y)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.loadButton = tk.Button(self, text='Load a graph\n from file', command=self.load)
        self.loadButton.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W, rowspan=2)
        self.dynamicButton = tk.Button(self, text='Dynamic', command=self.exec_dynamic)
        self.dynamicButton.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        self.dijkstraButton = tk.Button(self, text='Dijkstra', command=self.exec_dijkstra)
        self.dijkstraButton.grid(row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
        self.dial_dijkstraButton = tk.Button(self, text='Dial Dijkstra', command=self.exec_dial_dijkstra)
        self.dial_dijkstraButton.grid(row=0, column=3, sticky=tk.N + tk.S + tk.E + tk.W)
        self.radix_heap_dijkstraButton = tk.Button(self, text='Radix Heap Dijkstra',
                                                   command=self.exec_radix_heap_dijkstra)
        self.radix_heap_dijkstraButton.grid(row=0, column=4, sticky=tk.N + tk.S + tk.E + tk.W)
        self.label_correctingButton = tk.Button(self, text='Label Correcting', command=self.exec_label_correcting)
        self.label_correctingButton.grid(row=0, column=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.fifo_label_correctingButton = tk.Button(self, text='FIFO L.C.',
                                                     command=self.exec_fifo_label_correcting)
        self.fifo_label_correctingButton.grid(row=0, column=6, sticky=tk.N + tk.S + tk.E + tk.W)
        self.deque_label_correctingButton = tk.Button(self, text='Deque L.C.',
                                                      command=self.exec_deque_label_correcting)
        self.deque_label_correctingButton.grid(row=0, column=7, sticky=tk.N + tk.S + tk.E + tk.W)
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=0, column=8, sticky=tk.N + tk.S + tk.E + tk.W)
        self.resultText = tk.Text(self)  # , width=40, height=10)
        self.resultText.grid(row=3, column=0, sticky=tk.N + tk.S + tk.E + tk.W, columnspan=9)
        self.entry_label = tk.Label(self, text='Number of test cycles')
        self.entry_label.grid(row=4, column=0)
        self.entry = tk.Entry(self, justify=tk.CENTER)
        self.entry.insert(0, '100')
        self.entry.grid(row=4, column=1)
        self.mf_labeling_Button = tk.Button(self, text='M.F. Labeling', command=self.exec_mf_labeling)
        self.mf_labeling_Button.grid(row=1, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        self.mf_pre_flow_push_Button = tk.Button(self, text='M.F. PreFlow Push', command=self.exec_mf_pre_flow_push)
        self.mf_pre_flow_push_Button.grid(row=1, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
        self.mcf_successive_shortest_path_Button = tk.Button(self, text='M.C.F. Succ Shortest Path', command=self.exec_mcf_successive_shortest_path)
        self.mcf_successive_shortest_path_Button.grid(row=1, column=3, sticky=tk.N + tk.S + tk.E + tk.W)
        self.mcf_cycle_canceling_Button = tk.Button(self, text='M.C.F. Cycle Canceling', command=self.exec_mcf_cycle_canceling)
        self.mcf_cycle_canceling_Button.grid(row=1, column=4, sticky=tk.N + tk.S + tk.E + tk.W)
        self.neg_check_spp_Button = tk.Button(self, text='Neg. Cycle SPP', command=self.exec_neg_check_spp)
        self.neg_check_spp_Button.grid(row=1, column=5, sticky=tk.N + tk.S + tk.E + tk.W)
        icon = tk.PhotoImage(file="Logo_UniCa_64.png")
        top.tk.call("wm", "iconphoto", top._w, icon)

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
                result = result + test(int(self.entry.get()), self.graph, dynamic)
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
                result = result + test(int(self.entry.get()), self.graph, dijkstra)
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
                result = result + test(int(self.entry.get()), self.graph, dial_dijkstra)
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
                result = result + test(int(self.entry.get()), self.graph, radix_heap_dijkstra)
            self.resultText.insert(tk.INSERT, result)
        else:
            self.resultText.insert(tk.INSERT, "Graph not loaded")

    def exec_label_correcting(self):
        self.resultText.delete('1.0', tk.END)
        if self.graph is not None:
            g = label_correcting(dcp(self.graph))
            result = print_result(g, "Label Correcting")
            if g.neg_cycle:
                self.resultText.insert(tk.INSERT, result)
                return
            result = result + test(int(self.entry.get()), self.graph, label_correcting)
            self.resultText.insert(tk.INSERT, result)
        else:
            self.resultText.insert(tk.INSERT, "Graph not loaded")

    def exec_fifo_label_correcting(self):
        self.resultText.delete('1.0', tk.END)
        if self.graph is not None:
            g = fifo_label_correcting(dcp(self.graph))
            result = print_result(g, "FIFO Label Correcting")
            if g.neg_cycle:
                self.resultText.insert(tk.INSERT, result)
                return
            result = result + test(int(self.entry.get()), self.graph, fifo_label_correcting)
            self.resultText.insert(tk.INSERT, result)
        else:
            self.resultText.insert(tk.INSERT, "Graph not loaded")

    def exec_deque_label_correcting(self):
        self.resultText.delete('1.0', tk.END)
        if self.graph is not None:
            g = deque_label_correcting(dcp(self.graph))
            result = print_result(g, "Deque Label Correcting")
            if g.neg_cycle:
                self.resultText.insert(tk.INSERT, result)
                return
            result = result + test(int(self.entry.get()), self.graph, deque_label_correcting)
            self.resultText.insert(tk.INSERT, result)
        else:
            self.resultText.insert(tk.INSERT, "Graph not loaded")

    def exec_mf_labeling(self):
        self.resultText.delete('1.0', tk.END)
        if self.graph is not None:
            g = labeling(dcp(self.graph))
            result = print_result2(g, "MF Labeling")
            result = result + test(int(self.entry.get()), self.graph, labeling)
            self.resultText.insert(tk.INSERT, result)
            (paths, cycles) = flow_decomposition(g)
            result = print_result4(paths, cycles)
            self.resultText.insert(tk.INSERT, result)
        else:
            self.resultText.insert(tk.INSERT, "Graph not loaded")

    def exec_mf_pre_flow_push(self):
        self.resultText.delete('1.0', tk.END)
        if self.graph is not None:
            g = pre_flow_push(dcp(self.graph))
            result = print_result2(g, "MF PreFlow Push")
            result = result + test(int(self.entry.get()), self.graph, pre_flow_push)
            self.resultText.insert(tk.INSERT, result)
            (paths, cycles) = flow_decomposition(g)
            result = print_result4(paths, cycles)
            self.resultText.insert(tk.INSERT, result)
        else:
            self.resultText.insert(tk.INSERT, "Graph not loaded")

    def exec_mcf_successive_shortest_path(self):
        self.resultText.delete('1.0', tk.END)
        if self.graph is not None:
            g = successive_shortest_path(dcp(self.graph))
            result = print_result3(g, "MCF Successive Shortest Path")
            if g.mcf_error:
                self.resultText.insert(tk.INSERT, "Error in finding base feasible solution")
                return
            elif g.not_feasible:
                self.resultText.insert(tk.INSERT, "No feasible solution")
                return
            elif g.neg_cycle:
                self.resultText.insert(tk.INSERT, result)
                return
            else:
                result = result + test(int(self.entry.get()), self.graph, successive_shortest_path)
                self.resultText.insert(tk.INSERT, result)
                (paths, cycles)= flow_decomposition(g)
                result = print_result4(paths, cycles)
                self.resultText.insert(tk.INSERT, result)
        else:
            self.resultText.insert(tk.INSERT, "Graph not loaded")

    def exec_mcf_cycle_canceling(self):
        self.resultText.delete('1.0', tk.END)
        if self.graph is not None:
            g = cycle_canceling(dcp(self.graph))
            result = print_result5(g, "MCF Cycle Canceling")
            if g.mcf_error:
                self.resultText.insert(tk.INSERT, "Error in finding base feasible solution")
                return
            elif g.not_feasible:
                self.resultText.insert(tk.INSERT, "No feasible solution")
                return
            elif g.neg_cycle:
                self.resultText.insert(tk.INSERT, result)
                return
            else:
                result = result + test(int(self.entry.get()), self.graph, cycle_canceling)
                self.resultText.insert(tk.INSERT, result)
                (paths, cycles) = flow_decomposition(g)
                result = print_result4(paths, cycles)
                self.resultText.insert(tk.INSERT, result)
        else:
            self.resultText.insert(tk.INSERT, "Graph not loaded")

    def exec_neg_check_spp(self):
        self.resultText.delete('1.0', tk.END)
        if self.graph is not None:
            g = neg_check_label_correcting(dcp(self.graph))
            result = neg_check_print_result(g, "Neg. Check Label Correcting")
            result = result + test(int(self.entry.get()), self.graph, neg_check_label_correcting)
            self.resultText.insert(tk.INSERT, result)
        else:
            self.resultText.insert(tk.INSERT, "Graph not loaded")



app = App()
app.master.title('Network Flows Optimization')
app.mainloop()
