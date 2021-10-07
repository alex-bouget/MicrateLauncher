from tkinter import *
from .DataMenu import DataMenu
from .Lang import lang


class VersionMenu(DataMenu):
    class Versionner(DataMenu.Dataer):
        def __init__(self, root, version_color, version_name, callback):
            super().__init__(root, version_color)
            self.Callback = callback
            self.VersionName = version_name
            self.VersionNameLabel = Label(self, text=version_name, bg=version_color)
            self.UseButton = Button(self, text=lang["Text"]["Much"][0], font=(lang["Font"][1], 40), bg=version_color,
                                    command=self.Use)
            self.VersionNameLabel.place(x=4, y=4)
            self.pack()

        def Use(self):
            self.Callback["Use"](self.VersionName)

        def reload(self):
            self.DataReload()
            self.UseButton.place(x=self.winfo_width() // 2.6, y=self.winfo_height() // 6.7)

    def __init__(self, root, version_color, version_system):
        super().__init__(root, version_color)
        self.Color = version_color
        self.VersionSystem = version_system
        self.Version = []
        self.ButtonCanvas = Canvas(self, bg=version_color)
        self.Button = []
        for VersionType in ["installed", "release", "snapshot", "old_beta", "old_alpha"]:
            self.Button.append(Button(self.ButtonCanvas, text=VersionType, bg=version_color,
                                      command=lambda version=VersionType: self.ReloadFrame(version)))
            self.Button[-1].pack(side=LEFT, expand=YES, fill=Y)
        self.ReloadFrame("release")

    def ReloadFrame(self, version_type):
        for version in self.Version:
            version.destroy()
        del self.Version
        self.Version = []
        if version_type == "installed":
            for VersionName in self.VersionSystem.allInstalledVersion():
                self.Version.append(
                    VersionMenu.Versionner(self.Frame, self.Color, VersionName, {"Use": self.VersionSystem.setVersion}))
        else:
            for VersionName in [VersionID["id"] for VersionID in self.VersionSystem.allVersion() if
                                VersionID["type"] == version_type]:
                self.Version.append(
                    VersionMenu.Versionner(self.Frame, self.Color, VersionName, {"Use": self.VersionSystem.setVersion}))
        self.r = 0
        self.reload()

    def reload(self):
        for version in self.Version:
            version.reload()
        self.DataReload()
        self.ButtonCanvas.place(x=self.winfo_width() // 2, y=5, anchor=N)
        self.TagCanvas.configure(scrollregion=(0, 0, 0, (self.TagCanvas.winfo_height() // 1.7) * len(self.Version)))
