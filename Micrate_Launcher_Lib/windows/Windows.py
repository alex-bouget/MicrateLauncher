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


class MicrateWindow:
    """Windows for Micrate Launcher
    With Tkinter module

    :param Tk root:
    :param Lib system_lib:
    :param dict color_lib:
    """

    def __init__(self, root, system_lib, color_lib):
        self.ColorLib = color_lib
        self.SystemLib = system_lib
        self.root = root
        self.Main = MainMenu(root, color_lib["Main"], color_lib["Play"])
        self.old_h = 0
        self.old_w = 0
        self.Page = {
            "Version": VersionMenu(root, color_lib["Version"], system_lib.Version),
            "Profile": ProfileMenu(root, color_lib["Profile"], system_lib.Profile),
            "Session": SessionMenu(root, color_lib["Session"], system_lib.Session),
            "LoadBar": LoadingBar(root, color_lib["Loading"]),
            "Config": ConfigMenu(root, color_lib["Config"], system_lib),
            "Asker": UselessAsker(root, color_lib["Useless"])
        }
        UselessAsker.Asker = self.Page["Asker"]

        self.Main.JVMButton.configure(command=self.jvm)
        self.Main.PlayButton.configure(command=self.play)
        self.Page["Config"].CreateConfig.configure(command=self.create_config)
        self.ButtonCanvas = Canvas(self.Main)
        self.Button = []
        for button in [  # Button upper windows
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

    def create_config(self):
        """create a new config"""
        string = UselessAsker.Asker.get(True, "name")
        self.SystemLib.create_config(string["name"])
        self.Page["Config"].ReloadFrame()

    def jvm(self):
        """change jvm argument"""
        string = UselessAsker.Asker.get(True,
                                        JVM=open(os.path.join(self.SystemLib.SettingsFolder, "JVMarg.txt")).read())
        open(os.path.join(self.SystemLib.SettingsFolder, "JVMarg.txt"), "w").write(string["JVM"])

    def play(self):
        """play function for the button"""
        for widget in self.Main.winfo_children() + self.Button:  # desactive widget
            widget.configure(state="disabled")
        self.Page["LoadBar"].reload()
        self.SystemLib.start_mc({"setStatus": self.Page["LoadBar"].setStatus,
                                 "setMax": self.Page["LoadBar"].setMax,
                                 "setProgress": self.Page["LoadBar"].setProgress,
                                 "Finish": self.play_finish})

    def play_finish(self, arg):
        """open minecraft with argument

        :param list arg:
        """
        self.root.unbind("<Configure>")
        Popen(arg)
        self.root.destroy()

    def unplace(self):
        """disabled all opened page, for view main page"""
        for Page in self.Page.values():
            Page.place_forget()
        try:
            self.Main.LabelInfo[0].configure(
                text=lang["Text"]["MainMenu"][1] + self.SystemLib.Profile.login_data["selectedProfile"]["name"])
        except:
            pass
        try:
            self.Main.LabelInfo[1].configure(text=lang["Text"]["MainMenu"][2] + self.SystemLib.Session.get_session())
        except:
            pass
        try:
            self.Main.LabelInfo[2].configure(text=lang["Text"]["MainMenu"][3] + self.SystemLib.Version.version)
        except:
            pass

    def place(self, classe):
        """place a page

        :param str classe: id of the page
        """
        self.unplace()
        self.Page[classe].reload()

    def reload(self, evt):
        """Reload windows"""
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
