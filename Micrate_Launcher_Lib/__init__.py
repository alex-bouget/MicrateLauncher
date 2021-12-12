from tkinter import Tk, Event
import sys
import os
from .Lang import lang
from .Lib.MM1_Lib.folders import SuperFolders
from .Lib import MicrateLib
from .windows import MicrateWindow


"""Window of the Micrate Launcher"""


class MicrateLauncher(Tk):
    Folders: SuperFolders
    """All Folder needed for the launcher,
    accounts, java, Minecraft, session, settings"""
    Color: dict
    """All Color for each canvas, findable in Ressources/lang/*.json"""
    Lib: MicrateLib
    """Library of the launcher"""
    Windows: MicrateWindow
    """Canvas for the launcher"""

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.Folders = SuperFolders()
        self.iconbitmap("Ressources/ico.ico")
        self.title(lang["Text"]["Title"])
        self.configure(height=480, width=720)
        self.Color = lang["Color"]
        if len(sys.argv) > 1:  # decode arguments
            argument = sys.argv
            del argument[0]
            dico = {}
            for arg in argument:
                dico[arg.split("=")[0]] = arg.split("=")[1]
            for folders in ["accounts", "session", "Minecraft", "java", "settings"]:
                try:  # add the folder or use default folders for each argument
                    self.Folders.add_folder(folders, dico[folders])
                except KeyError:
                    self.Folders.add_folder(folders, folders)
        else:  # use default folder
            for folders in ["accounts", "session", "Minecraft", "java", "settings"]:
                self.Folders.add_folder(folders, folders)
        self.Lib = MicrateLib(self.Folders.get_folder("accounts"),
                              self.Folders.get_folder("session"),
                              self.Folders.get_folder("Minecraft"),
                              self.Folders.get_folder("java"),
                              self.Folders.get_folder("settings"),
                              )  # load Micrate library
        #  create default file
        if os.path.isfile(os.path.join(self.Folders.get_folder("settings"), "config.txt")):
            self.Lib.set_config(open(os.path.join(self.Folders.get_folder("settings"), "config.txt")).read())
        if not os.path.isfile(os.path.join(self.Folders.get_folder("Minecraft"), "Launcher_profiles.json")):
            open(os.path.join(self.Folders.get_folder("Minecraft"), "Launcher_profiles.json"), "w").write(
                "{}")
        if not os.path.isfile(os.path.join(self.Folders.get_folder("settings"), "JVMarg.txt")):
            open(os.path.join(self.Folders.get_folder("settings"), "JVMarg.txt"), "w").write(
                "-Xmx2G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20" +
                " -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M")

        self.Windows = MicrateWindow(self, self.Lib, self.Color)  # load Micrate windows
        self.bind("<Configure>", self.reload)

    def reload(self, evt: Event or None):
        """Reload all window"""
        self.Windows.reload(evt)  # Reload Canvas in the window

    def start_launcher(self):
        """launch the tkinter's mainloop()."""
        self.mainloop()
        sys.exit()
