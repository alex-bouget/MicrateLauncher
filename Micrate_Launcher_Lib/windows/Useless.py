from tkinter import *
from .Lang import lang
from .DataMenu import DataMenu2


class UselessAsker(DataMenu2):
    Asker = ""

    def __init__(self, root, color):
        self.color = color
        super().__init__(root, self.color)
        self.root = root
        self.Data = Canvas(self, bg=self.color)

        self.reload()

    def get(self, entry=True, *arg, **kwargs):
        self.entry = entry
        self.Enter = []
        self.key_return = []
        for key in arg:
            self.key_return.append(key)
            self.placeData(key, "", len(self.key_return) - 1)
        for key, value in kwargs.items():
            self.key_return.append(key)
            self.placeData(key, value, len(self.key_return) - 1)

        Button(self.Data, bg=self.color, text=lang["Text"]["Much"][6], command=self.finish).grid(
            row=len(self.key_return), column=0)

        self.reload()

        self.mainloop()

        if self.entry:
            return self.Return

    def finish(self):
        if self.entry:
            self.Return = {}
            for number in range(len(self.key_return)):
                self.Return[self.key_return[number]] = self.Enter[number].get()
        self.Data.destroy()
        self.Data = Canvas(self, bg=self.color)
        self.place_forget()
        self.quit()

    def placeData(self, name, value, row):
        Label(self.Data, text=name, bg=self.color).grid(row=row, column=0)
        if self.entry:
            self.Enter.append(Entry(self.Data, bg=self.color))
            self.Enter[-1].delete(0, END)
            self.Enter[-1].insert(0, value)
            if name == lang["Text"]["ProfileMenu"][3]:
                self.Enter[-1].configure(show="*")
            self.Enter[-1].grid(row=row, column=1)

    def reload(self):
        self.DataReload()
        self.Data.place(x=self.winfo_width() // 2, y=self.winfo_height() // 2, anchor=CENTER)
