from tkinter import *


class DataMenu(Canvas):
    class Dataer(Canvas):
        def __init__(self, master, color):
            super().__init__(master, bg=color)

        def DataReload(self):
            self.configure(height=self.master.master.winfo_height() // 1.9,
                           width=self.master.master.winfo_width() // 1.1)

    def __init__(self, master, color):
        super().__init__(master, bg=color)
        self.TagCanvas = Canvas(self, bg=color)
        self.Frame = Frame(self.TagCanvas, bg=color)
        self.TagCanvas.create_window(0, 0, anchor='nw', window=self.Frame)
        self.bar = Scrollbar(self, command=self.TagCanvas.yview, orient="vertical")
        self.bar.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.TagCanvas.configure(yscrollcommand=self.bar.set)
        self.bind("<MouseWheel>", self.Mouse)

    def Mouse(self, event):
        if self.winfo_ismapped():
            self.TagCanvas.yview("scroll", int(-1 * (event.delta / 120)), "units")

    def DataReload(self):
        self.configure(height=self.master.winfo_height() // 1.1, width=self.master.winfo_width() - 5)
        self.TagCanvas.configure(height=self.winfo_height() // 1.13, width=self.winfo_width() // 1.36)
        self.place(x=0, y=self.master.winfo_height() // 9.6)
        self.TagCanvas.place(x=4, y=self.winfo_height() // 7.6)


class DataMenu2(Canvas):
    def __init__(self, master, color):
        super().__init__(master, bg=color)

    def DataReload(self):
        self.configure(height=self.master.winfo_height() // 2, width=self.master.winfo_height() // 1.05)
        self.place(anchor=CENTER, x=self.master.winfo_width() // 2, y=self.master.winfo_height() // 2)
