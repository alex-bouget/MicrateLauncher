from tkinter import *
import os
from subprocess import Popen
from .Lang import lang
from .Useless import UselessAsker
from .MainMenu import MainMenu
from .VersionMenu import VersionMenu
from .ProfileMenu import ProfileMenu
from .SessionMenu import SessionMenu
from .LoadingBar import LoadingBar
from .ConfigMenu import ConfigMenu


class Micrate_Window:
    def __init__(self, root, SystemLib, ColorLib):
        self.ColorLib = ColorLib
        self.SystemLib = SystemLib
        self.root = root
        self.Main = MainMenu(root, ColorLib["Main"], ColorLib["Play"])
        self.Page = {
            "Version": VersionMenu(root, ColorLib["Version"], SystemLib.Version),
            "Profile": ProfileMenu(root, ColorLib["Profile"], SystemLib.Profile),
            "Session": SessionMenu(root, ColorLib["Session"], SystemLib.Session),
            "LoadBar": LoadingBar(root, ColorLib["Loading"]),
            "Config": ConfigMenu(root, ColorLib["Config"], SystemLib),
            "Asker": UselessAsker(root, ColorLib["Useless"])
        }
        UselessAsker.Asker = self.Page["Asker"]

        self.Main.JVMButton.configure(command=self.JVM)
        self.Main.PlayButton.configure(command=self.play)
        self.Page["Config"].CreateConfig.configure(command=self.createconfig)
        self.ButtonCanvas = Canvas(self.Main)
        self.Button = []
        for button in [
            [lang["Text"]["MainMenu"][4], self.unplace],
            [lang["Text"]["MainMenu"][5], lambda: self.place("Profile")],
            [lang["Text"]["MainMenu"][6], lambda: self.place("Session")],
            [lang["Text"]["MainMenu"][7], lambda: self.place("Version")],
            [lang["Text"]["MainMenu"][8], lambda: self.place("Config")]
        ]:
            self.Button.append(Button(self.ButtonCanvas, text=button[0], bg=lang["Color"]["Button"], command=button[1],
                                      font=(lang["Font"][1], 15)))
            self.Button[-1].pack(side=LEFT, expand=YES, fill=Y)
        self.name = ""
        self.reload(None)
        self.unplace()
    def createconfig(self):
        string = UselessAsker.Asker.get(True, "name")
        self.SystemLib.createConfig(string["name"])
        self.Page["Config"].ReloadFrame()

    def JVM(self):
        string = UselessAsker.Asker.get(True,
                                        JVM=open(os.path.join(self.SystemLib.SettingsFolder, "JVMarg.txt")).read())
        open(os.path.join(self.SystemLib.SettingsFolder, "JVMarg.txt"), "w").write(string["JVM"])

    def play(self):
        for widget in self.Main.winfo_children() + self.Button:
            widget.configure(state="disabled")
        self.Page["LoadBar"].reload()
        self.SystemLib.startMC({"setStatus": self.Page["LoadBar"].setStatus,
                                "setMax": self.Page["LoadBar"].setMax,
                                "setProgress": self.Page["LoadBar"].setProgress,
                                "Finish": self.play_finish})

    def play_finish(self, arg):
        self.root.unbind("<Configure>")
        Popen(arg)
        self.root.destroy()

    def unplace(self):
        for Page in self.Page.values():
            Page.place_forget()
        try:
            self.Main.LabelInfo[0].configure(
                text=lang["Text"]["MainMenu"][1] + self.SystemLib.Profile.login_data["selectedProfile"]["name"])
        except:
            pass
        try:
            self.Main.LabelInfo[1].configure(text=lang["Text"]["MainMenu"][2] + self.SystemLib.Session.getSession())
        except:
            pass
        try:
            self.Main.LabelInfo[2].configure(text=lang["Text"]["MainMenu"][3] + self.SystemLib.Version.version)
        except:
            pass

    def place(self, classe):
        self.unplace()
        self.Page[classe].reload()

    def reload(self, evt):
        try:
            if self.SystemLib.Profile.login_data['selectedProfile']['name'] != self.name:
                self.Main.Image(self.SystemLib.Profile.login_data['selectedProfile']['name'])
                self.name = self.SystemLib.Profile.login_data['selectedProfile']['name']
        except:
            pass
        if evt is None:
            self.Main.reload()
            self.ButtonCanvas.place(anchor=N, x=self.Main.winfo_width() // 2, y=5)
            for Page in self.Page.values():
                if Page.winfo_ismapped():
                    Page.reload()
        elif str(evt.widget) == ".":
            self.Main.reload()
            self.ButtonCanvas.place(anchor=N, x=self.Main.winfo_width() // 2, y=5)
            for Page in self.Page.values():
                if Page.winfo_ismapped():
                    Page.reload()
        else:
            try:
                evt.widget.reload()
            except:
                pass