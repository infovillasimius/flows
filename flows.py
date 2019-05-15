import tkinter as tk


class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.createWidgets()

    def createWidgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)


app = App()
app.master.title('Prova')
# app.mainloop()

try:
    stream = open("mcfGraph.txt", "rt")
    numbers = []

    lines = stream.readlines()
    for l in lines:
        for s in l.split():
            numbers.append(int(s))
    stream.close()
except Exception as exc:
    print("Cannot open the file:", exc)

print(numbers)
