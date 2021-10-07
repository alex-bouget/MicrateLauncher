from tkinter import *
from .DataMenu import DataMenu2
from tkinter.ttk import Progressbar


class LoadingBar(DataMenu2):
    def __init__(self, master, load_color):
        super().__init__(master, load_color)
        self.Bar = Progressbar(self, orient=HORIZONTAL, length=100, mode="determinate")
        self.stats = StringVar()
        self.Max = 1
        self.Progress = 0
        self.Text = Label(self, textvariable=self.stats, bg=load_color)
        self.text = ""
        self.Bar.place(relx=0, rely=0, anchor=NW, relwidth=1, relheight=0.7)
        self.Text.place(relx=0, rely=1, anchor=SW, relwidth=1, relheight=0.3)
        self.reload()
        self.after(500, self._setStatus)

    def setStatus(self, text):
        self.text = text

    def _setStatus(self):
        self.stats.set(self.text)
        self.reloadStat()
        self.after(500, self._setStatus)

    def setMax(self, maximum):
        self.Max = maximum

    def setProgress(self, progress):
        self.Progress = progress

    def reloadStat(self):
        self.Bar["value"] = int((self.Progress / self.Max) * 100)

    def reload(self):
        self.DataReload()
