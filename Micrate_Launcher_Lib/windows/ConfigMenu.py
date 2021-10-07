from tkinter import *
import tkinter.messagebox as messagebox
from .DataMenu import DataMenu
from .Lang import lang


class ConfigMenu(DataMenu):
    class Configer(DataMenu.Dataer):
        def __init__(self, master, config_color, config_name, config_arg, callback):
            super().__init__(master, config_color)
            self.Callback = callback
            self.ConfigName = config_name
            self.Config_arg = config_arg
            self.ConfigNameLabel = Label(self, text=self.ConfigName + "\n" + " | ".join(config_arg), bg=config_color)
            self.UseButton = Button(self, text=lang["Text"]["Much"][0], font=(lang["Font"][1], 40), bg=config_color,
                                    command=self.Use)
            self.DeleteButton = Button(self, text=lang["Text"]["Much"][1], bg=config_color, command=self.Delete)
            self.ConfigNameLabel.place(x=4, y=4)
            self.pack()

        def Delete(self):
            if messagebox.askyesno(lang["Text"]["Much"][2],
                                   lang["Text"]["Much"][3] + self.ConfigName + lang["Text"]["Much"][4]):
                self.Callback["Delete"](self.ConfigName)
                self.Callback["Refresh"]()

        def Use(self):
            self.Callback["Use"](self.ConfigName)

        def reload(self):
            self.DataReload()
            self.UseButton.place(x=self.winfo_width() // 2.6, y=self.winfo_height() // 6.7)

    def __init__(self, master, config_color, config_system):
        super().__init__(master, config_color)
        self.Color = config_color
        self.ConfigSystem = config_system
        self.Config = []
        self.CreateConfig = Button(self, text=lang["Text"]["ConfigMenu"][0], bg=config_color)
        self.ReloadFrame()

    def ReloadFrame(self):
        for config in self.Config:
            config.destroy()
        self.Config = []
        for name, value in self.ConfigSystem.getAllConfig():
            self.Config.append(ConfigMenu.Configer(self.Frame, self.Color, name, value,
                                                   {"Refresh": self.ReloadFrame,
                                                    "Delete": self.ConfigSystem.deleteConfig,
                                                    "Use": self.ConfigSystem.setConfig}))

    def reload(self):
        for config in self.Config:
            config.reload()
        self.DataReload()
        self.CreateConfig.place(x=self.winfo_width() // 1.3, y=4)
        self.TagCanvas.configure(scrollregion=(0, 0, 0, (self.TagCanvas.winfo_height() // 1.7) * len(self.Config)))
