from tkinter import *
from ..Lang import lang
from urllib.request import Request, urlopen
from PIL import Image, ImageTk
from .Useless import UselessAsker


class MainMenu(Canvas):
    def __init__(self, root, play_color, main_color):
        super().__init__(master=root, bg=main_color)
        self.PlayButton = Button(self, text=lang["Text"]["MainMenu"][0], font=(lang["Font"][0], 40), bg=play_color)
        self.CreditButton = Button(self, text=lang["Text"]["MainMenu"][9], command=self.credit, bg=main_color)
        self.JVMButton = Button(self, text=lang["Text"]["MainMenu"][10], bg=main_color)
        self.PlayButton.place(relx=0, rely=1, anchor=SW, relwidth=1)
        self.LabelInfo = []
        for i in range(4):
            self.LabelInfo.append(Label(self, bg=main_color))
        self.place(x=0, y=0)

    def Image(self, account_name):
        if lang["Perspective"] == "yes":
            self.ImageHead = Image.open(urlopen(
                Request("https://minotar.net/cube/" + account_name + "/512.png",
                        headers={'User-Agent': 'Mozilla/5.0'})))
        else:
            self.ImageHead = Image.open(urlopen(Request("https://minotar.net/avatar/" + account_name + "/512.png",
                                                        headers={'User-Agent': 'Mozilla/5.0'})))

    @staticmethod
    def credit():
        UselessAsker.Asker.get(False, "coder: MisterMine01", "Helper: Dalgol", "head Api: Cravatar\ncopyright 2020")

    def reload(self):
        self.configure(width=self.master.winfo_width(), height=self.master.winfo_height())
        try:
            try:
                self.ImageResize = ImageTk.PhotoImage(
                    self.ImageHead.resize((int(self.winfo_height() * 0.4), int(self.winfo_height() * 0.4))))
            except ValueError:
                self.ImageResize = ImageTk.PhotoImage(self.ImageHead.resize((1, 1)))
            self.LabelInfo[3].configure(image=self.ImageResize)
        except AttributeError:
            pass
        for i in range(3):
            self.LabelInfo[i].place(x=4, y=(self.winfo_height() // 6.4) + (self.winfo_height() // 19.2) * i)
        self.LabelInfo[3].place(x=self.winfo_width() // 1.8, y=self.winfo_height() // 6.4)
        self.CreditButton.place(x=4, y=self.winfo_height() // 2.3)
        self.JVMButton.place(x=4, y=self.winfo_height() // 2)