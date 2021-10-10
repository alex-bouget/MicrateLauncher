from .jdk import install as jdk_install
from .Profile import ProfileLib
from .Session import SessionLib
from .Version import VersionLib
from .Mcl_lib import install, command
from threading import Thread
import os
import json


def empty(arg):
    """ empty function for exception

    :param arg:
    """
    pass


class MicrateLib:
    """Library for Micrate Launcher

    :param str profile_folder: folder where profile was save
    :param str session_folder: folder where session was save
    :param str minecraft_folder: folder where minecraft was downloaded
    :param str java_folder: folder where java was downloaded
    :param str settings_folder: folder where settings was save
    """
    def __init__(self, profile_folder, session_folder, minecraft_folder, java_folder, settings_folder):
        self.MinecraftFolder = minecraft_folder
        self.JavaFolder = java_folder
        self.SessionFolder = session_folder
        self.ProfileFolder = profile_folder
        self.SettingsFolder = settings_folder
        self.Profile = ProfileLib(profile_folder, settings_folder)
        self.Version = VersionLib(minecraft_folder)
        self.Session = SessionLib(session_folder)

    def start_mc(self, callback):
        """Start Minecraft

        Get login_data, session and the version, download java and Minecraft and start the Game

        :param dict callback: callback for display information (Finish, setStatus, setProgress, setMax)
        :return:
        """
        self.SettingsStarting = [self.Profile.login_data, self.Session.getSession(), self.Version.version]

        def start(micrate_self, call_back):
            if len(os.listdir(micrate_self.JavaFolder)) == 0:
                jdk_install(version="8", Callback=call_back, _JDK_DIR=micrate_self.JavaFolder)
            install.install_minecraft_version(micrate_self.SettingsStarting[2], micrate_self.MinecraftFolder, call_back)
            micrate_command = command.get_minecraft_command(micrate_self.SettingsStarting[2],
                                                            micrate_self.MinecraftFolder,
                                                            {"username": micrate_self.SettingsStarting[0][
                                                                "selectedProfile"]["name"],
                                                             "uuid": micrate_self.SettingsStarting[0][
                                                                 "selectedProfile"]["id"],
                                                             "token": micrate_self.SettingsStarting[0]["accessToken"],
                                                             "executablePath": os.path.join(
                                                                 micrate_self.JavaFolder, os.listdir(
                                                                     micrate_self.JavaFolder)[0], "bin", "java"),
                                                             "launcherName": "Micrate_Launcher",
                                                             "launcherVersion": "2.0",
                                                             "gameDirectory": os.path.join(micrate_self.SessionFolder,
                                                                                           micrate_self.
                                                                                           SettingsStarting[1]),
                                                             "jvmArguments": open(os.path.join(micrate_self.
                                                                                               SettingsFolder,
                                                                                               "JVMarg.txt")).read().
                                                            split(" ")
                                                             })
            call_back.get("Finish", empty)(micrate_command)

        thread = Thread(target=lambda call=callback: start(self, call))
        thread.daemon = True
        thread.start()

    def create_config(self, name):
        """Create a game config (user, session, version)

        :param str name: name of the new config
        """
        settings_config = [self.Profile.login_data["selectedProfile"]["name"], self.Session.getSession(),
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

    def set_config(self, name):
        """Load a config

        :param str name: Name of the config
        """
        config = json.load(open(os.path.join(self.SettingsFolder, "config.json")))
        if config.get(name) is not None:
            settings_config = config[name]
            self.Profile.setProfile(
                [
                    key
                    for key, value in self.Profile.allProfile().items()
                    if value == settings_config[0]
                ][0]
            )
            self.Session.setSession(settings_config[1])
            self.Version.setVersion(settings_config[2])
            with open(os.path.join(self.SettingsFolder, "config.txt"), "w") as file:
                file.write(name)

    def get_all_config(self):
        """ Get the saved config

        :return: list items of config
        """
        if os.path.isfile(os.path.join(self.SettingsFolder, "config.json")):
            return json.load(open(os.path.join(self.SettingsFolder, "config.json"))).items()
        else:
            return {}.items()

    def delete_config(self, name):
        """Delete a config

        :param str name: Name of config
        """
        if os.path.isfile(os.path.join(self.SettingsFolder, "config.json")):
            config = json.load(open(os.path.join(self.SettingsFolder, "config.json")))
            if config.get(name) is not None:
                del config[name]
                json.dump(open(os.path.join(self.SettingsFolder, "config.json"), "w"), config)
