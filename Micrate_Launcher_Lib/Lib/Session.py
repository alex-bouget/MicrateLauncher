import os
import shutil
from .Lang import lang


class SessionLib:
    def __init__(self, session_folder):
        self.folders = session_folder
        self.session = None

    def createSession(self, name_session):
        if not os.path.exists(os.path.join(self.folders, name_session)):
            os.mkdir(os.path.join(self.folders, name_session))
            self.session = name_session
        else:
            return ["NameError", lang["Text"]["Error"][0]]

    def deleteSession(self, name_session):
        if os.path.exists(os.path.join(self.folders, name_session)):
            shutil.rmtree(os.path.join(self.folders, name_session))
            if self.session == name_session:
                del self.session
        else:
            return ["NameError", lang["Text"]["Error"][1]]

    def setSession(self, name):
        if os.path.exists(os.path.join(self.folders, name)):
            self.session = name
        else:
            return ["NameError", lang["Text"]["Error"][1]]

    def getSession(self):
        return self.session

    def allSession(self):
        return os.listdir(self.folders)
