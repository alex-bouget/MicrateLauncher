import os
import shutil
from ..Lang import lang


"""Session Library for Micrate Launcher"""


class SessionLib:
    folders: str
    """folder where Session was save"""
    session: str or None
    """Session use now"""

    def __init__(self, session_folder: str):
        """constructor"""
        self.folders = session_folder
        self.session = None

    def create_session(self, name_session: str):
        """Create a new Session folder"""
        if not os.path.exists(os.path.join(self.folders, name_session)):
            os.mkdir(os.path.join(self.folders, name_session))
            self.session = name_session
        else:
            return ["NameError", lang["Text"]["Error"][0]]

    def delete_session(self, name_session: str):
        """Delete a session"""
        if os.path.exists(os.path.join(self.folders, name_session)):
            shutil.rmtree(os.path.join(self.folders, name_session))
            if self.session == name_session:
                del self.session
        else:
            return ["NameError", lang["Text"]["Error"][1]]

    def set_session(self, name: str):
        """Set a session"""
        if os.path.exists(os.path.join(self.folders, name)):
            self.session = name
        else:
            return ["NameError", lang["Text"]["Error"][1]]

    def get_session(self) -> str:
        """get actual session"""
        return self.session

    def all_session(self) -> list:
        """Return all session existed"""
        return os.listdir(self.folders)
