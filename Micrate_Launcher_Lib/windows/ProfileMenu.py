from tkinter import *
from .DataMenu import DataMenu
from ..Lang import lang
from urllib.request import Request, urlopen
from PIL import Image, ImageTk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
from .Useless import UselessAsker


class ProfileMenu(DataMenu):
    class Profiler(DataMenu.Dataer):
        def __init__(self, master, profile_color, account_id, account_name, callback):
            super().__init__(master, profile_color)
            self.Callback = callback
            self.AccountName = account_name
            self.AccountId = account_id
            self.AccountNameLabel = Label(self, text=account_name, font=(lang["Font"][0], 15), bg=profile_color)
            self.UseButton = Button(self, text=lang["Text"]["Much"][0], font=(lang["Font"][1], 40), bg=profile_color,
                                    command=self.Use)
            self.DeleteButton = Button(self, text=lang["Text"]["Much"][1], bg=profile_color, command=self.Delete)
            self.skinButton = Button(self, text=lang["Text"]["ProfileMenu"][0], bg=profile_color, command=self.Skin)
            self.Head = Label(self, bg=profile_color)
            self.ImageHead = self.Image()
            self.Head.place(x=2, y=2)
            self.pack()

        def Image(self):
            if lang["Perspective"] == "yes":
                return Image.open(urlopen(Request("https://minotar.net/cube/" + self.AccountName + "/1024.png",
                                                  headers={'User-Agent': 'Mozilla/5.0'})))
            else:
                return Image.open(urlopen(Request("https://minotar.net/avatar/" + self.AccountName + "/1024.png",
                                                  headers={'User-Agent': 'Mozilla/5.0'})))

        def reload(self):
            self.DataReload()
            try:
                self.ImageResize = ImageTk.PhotoImage(
                    self.ImageHead.resize((int(self.winfo_height() * 0.8), int(self.winfo_height() * 0.8))))
            except ValueError:
                self.ImageResize = ImageTk.PhotoImage(self.ImageHead.resize((1, 1)))
            self.Head.configure(image=self.ImageResize)
            self.AccountNameLabel.place(x=10, y=self.winfo_height() // 1.2)
            self.UseButton.place(x=self.winfo_width() // 2.6, y=self.winfo_height() // 6.7)
            self.DeleteButton.place(x=self.winfo_width() // 1.2, y=10)
            self.skinButton.place(x=self.winfo_width() // 2.6, y=self.winfo_height() // 1.25)

        def Delete(self):
            if messagebox.askyesno(lang["Text"]["Much"][2],
                                   lang["Text"]["Much"][3] + self.AccountName + lang["Text"]["Much"][4]):
                self.Callback["Delete"](self.AccountId)
                self.Callback["Refresh"]()

        def Use(self):
            self.Callback["Use"](self.AccountId)

        def Skin(self):
            self.Callback["Skin"](self.AccountName)

    def __init__(self, master, profile_color, profile_system):
        super().__init__(master, profile_color)
        self.ProfileSystem = profile_system
        self.Color = profile_color
        self.Profile = []
        self.CreateProfile = Button(self, text=lang["Text"]["ProfileMenu"][1], bg=profile_color, command=self.Create)
        self.ReloadFrame()

    def Skin(self, account_name):
        self.ProfileSystem.change_skin(filedialog.askopenfilename(defaultextension=".png"), account_name)

    def Create(self):
        profile = UselessAsker.Asker.get(True, lang["Text"]["ProfileMenu"][2], lang["Text"]["ProfileMenu"][3])
        self.ProfileSystem.create_profile(profile[lang["Text"]["ProfileMenu"][2]],
                                          profile[lang["Text"]["ProfileMenu"][3]])
        self.ReloadFrame()

    def ReloadFrame(self):
        for profile in self.Profile:
            profile.destroy()
        self.Profile = []
        for key, value in self.ProfileSystem.all_profile().items():
            self.Profile.append(
                ProfileMenu.Profiler(self.Frame, self.Color, key, value, {"Delete": self.ProfileSystem.delete_profile,
                                                                          "Refresh": self.ReloadFrame,
                                                                          "Use": self.ProfileSystem.set_profile,
                                                                          "Skin": self.Skin}
                                     ))
        self.reload()

    def reload(self):
        for profile in self.Profile:
            profile.reload()
        self.DataReload()
        self.CreateProfile.place(x=self.winfo_width() // 1.3, y=4)
        self.TagCanvas.configure(scrollregion=(0, 0, 0, (self.TagCanvas.winfo_height() // 1.7) * len(self.Profile)))
