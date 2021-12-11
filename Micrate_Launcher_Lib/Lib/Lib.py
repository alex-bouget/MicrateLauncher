from jdk import install as jdk_install
from .Profile import ProfileLib
from .Session import SessionLib
from .Version import VersionLib
from minecraft_launcher_lib import install, command
from threading import Thread
import os
import json


def empty(arg):
    """ empty function for exception"""
    pass


"""Library for Micrate Launcher"""


class MicrateLib:
    MinecraftFolder: str
    """Folder for the library"""
    JavaFolder: str
    """Folder for the library"""
    SessionFolder: str
    """Folder for the library"""
    ProfileFolder: str
    """Folder for the library"""
    SettingsFolder: str
    """Folder for the library"""
    Profile: ProfileLib
    """Library of the Profile"""
    Version: VersionLib
    """Library of the Version"""
    Session: SessionLib
    """Library of the Session"""
    settings_starting: list
    """List for start minecraft"""

    def __init__(self, profile_folder: str, session_folder: str,
                 minecraft_folder: str, java_folder: str, settings_folder: str):
        """Constructor"""
        self.MinecraftFolder = minecraft_folder
        self.JavaFolder = java_folder
        self.SessionFolder = session_folder
        self.ProfileFolder = profile_folder
        self.SettingsFolder = settings_folder
        self.Profile = ProfileLib(profile_folder, settings_folder)
        self.Version = VersionLib(minecraft_folder)
        self.Session = SessionLib(session_folder)

    def start_mc(self, callback: dict):
        """Start Minecraft
        Get login_data, session and the version, download java and Minecraft and start the Game
        """
        self.settings_starting = [self.Profile.login_data, self.Session.get_session(), self.Version.version]

        def start(micrate_self: MicrateLib, call_back: dict):
            if len(os.listdir(micrate_self.JavaFolder)) == 0:
                call_back["setStatus"]("Download Java")
                call_back["setMax"](1)
                call_back["setProgress"](0)
                jdk_install(version="8", path=micrate_self.JavaFolder)
            install.install_minecraft_version(micrate_self.settings_starting[2],
                                              micrate_self.MinecraftFolder, call_back)
            minecraft_command_data = {
                "username": micrate_self.settings_starting[0]["selectedProfile"]["name"],
                "uuid": micrate_self.settings_starting[0]["selectedProfile"]["id"],
                "token": micrate_self.settings_starting[0]["accessToken"],
                "executablePath": os.path.join(micrate_self.JavaFolder,
                                               os.listdir(micrate_self.JavaFolder)[0],
                                               "bin",
                                               "java"),
                "launcherName": "Micrate_Launcher",
                "launcherVersion": "2.0",
                "gameDirectory": os.path.join(micrate_self.SessionFolder,
                                              micrate_self.settings_starting[1]),
                "jvmArguments": open(os.path.join(micrate_self.SettingsFolder,
                                                  "JVMarg.txt")).read().split(" ")
            }

            micrate_command = command.\
                get_minecraft_command(micrate_self.settings_starting[2],
                                      micrate_self.MinecraftFolder,
                                      minecraft_command_data)
            call_back.get("Finish", empty)(micrate_command)

        thread = Thread(target=lambda call=callback: start(self, call))
        thread.daemon = True
        thread.start()

    def create_config(self, name: str):
        """Create a game config (user, session, version)"""
        settings_config = [self.Profile.login_data["selectedProfile"]["name"], self.Session.get_session(),
                           self.Version.version]
        if os.path.isfile(os.path.join(self.SettingsFolder, "config.json")):
            config = json.load(open(os.path.join(self.SettingsFolder, "config.json")))
            if config.get(name) is None:
                config[name] = settings_config
                json.dump(open(os.path.join(self.SettingsFolder, "config.json"), "w"), config)
                with open(os.path.join(self.SettingsFolder, "config.txt"), "w") as file:
                    file.write(name)
        else:
            dic = {name: settings_config}
            open(os.path.join(self.SettingsFolder, "config.json"), "w").write(json.dumps(dic))
            with open(os.path.join(self.SettingsFolder, "config.txt"), "w") as file:
                file.write(name)

    def set_config(self, name: str):
        """Load a config"""
        config = json.load(open(os.path.join(self.SettingsFolder, "config.json")))
        if config.get(name) is not None:
            settings_config = config[name]
            self.Profile.set_profile(
                [
                    key
                    for key, value in self.Profile.all_profile().items()
                    if value == settings_config[0]
                ][0]
            )
            self.Session.set_session(settings_config[1])
            self.Version.set_version(settings_config[2])
            with open(os.path.join(self.SettingsFolder, "config.txt"), "w") as file:
                file.write(name)

    def get_all_config(self) -> dict.items:
        """ Get the saved config"""
        if os.path.isfile(os.path.join(self.SettingsFolder, "config.json")):
            return json.load(open(os.path.join(self.SettingsFolder, "config.json"))).items()
        else:
            return {}.items()

    def delete_config(self, name: str):
        """Delete a config"""
        if os.path.isfile(os.path.join(self.SettingsFolder, "config.json")):
            config = json.load(open(os.path.join(self.SettingsFolder, "config.json")))
            if config.get(name) is not None:
                del config[name]
                json.dump(open(os.path.join(self.SettingsFolder, "config.json"), "w"), config)
