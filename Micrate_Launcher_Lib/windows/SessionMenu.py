from tkinter import *
from .DataMenu import DataMenu
import tkinter.messagebox as messagebox
from .Useless import UselessAsker
from ..Lang import lang


class SessionMenu(DataMenu):
    class Sessioner(DataMenu.Dataer):
        def __init__(self, master, session_color, session_name, callback):
            super().__init__(master, session_color)
            self.Callback = callback
            self.SessionName = session_name
            self.SessionNameLabel = Label(self, text=session_name, bg=session_color)
            self.UseButton = Button(self, text=lang["Text"]["Much"][0], font=(lang["Font"][1], 40), bg=session_color,
                                    command=self.Use)
            self.DeleteButton = Button(self, text=lang["Text"]["Much"][1], bg=session_color, command=self.Delete)
            self.SessionNameLabel.place(x=4, y=4)
            self.pack()

        def Delete(self):
            if messagebox.askyesno(lang["Text"]["Much"][2],
                                   lang["Text"]["Much"][3] + self.SessionName + lang["Text"]["Much"][4]):
                self.Callback["Delete"](self.SessionName)
                self.Callback["Refresh"]()

        def Use(self):
            self.Callback["Use"](self.SessionName)

        def reload(self):
            self.DataReload()
            self.UseButton.place(x=self.winfo_width() // 2.6, y=self.winfo_height() // 6.7)
            self.DeleteButton.place(x=self.winfo_width() // 1.2, y=10)

    def __init__(self, master, session_color, session_system):
        super().__init__(master, session_color)
        self.Color = session_color
        self.SessionSystem = session_system
        self.Session = []
        self.CreateSession = Button(self, text=lang["Text"]["SessionMenu"][0], bg=session_color, command=self.Create)
        self.ReloadFrame()

    def Create(self):
        session = UselessAsker.Asker.get(True, lang["Text"]["SessionMenu"][1])
        if session != "":
            self.SessionSystem.create_session(session[lang["Text"]["SessionMenu"][1]])
        self.ReloadFrame()

    def ReloadFrame(self):
        for session in self.Session:
            session.destroy()
        self.Session = []
        for SessionName in self.SessionSystem.all_session():
            self.Session.append(
                SessionMenu.Sessioner(self.Frame, self.Color, SessionName, {"Delete": self.SessionSystem.delete_session,
                                                                            "Refresh": self.ReloadFrame,
                                                                            "Use": self.SessionSystem.set_session}
                                      ))
        self.reload()

    def reload(self):
        for session in self.Session:
            session.reload()
        self.DataReload()
        self.CreateSession.place(x=self.winfo_width() // 1.3, y=4)
        self.TagCanvas.configure(scrollregion=(0, 0, 0, (self.TagCanvas.winfo_height() // 1.7) * len(self.Session)))
