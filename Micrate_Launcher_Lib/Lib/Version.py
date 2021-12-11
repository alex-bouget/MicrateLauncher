from .Mcl_lib import utils
import os


"""Minecraft Version library
get all version and all installed version"""


class VersionLib:
    MinecraftFolder: str
    """Folder where minecraft was downloaded"""
    version: str or None
    """Version loaded"""

    def __init__(self, minecraft_folder: str):
        """Constructor"""
        self.MinecraftFolder = minecraft_folder
        self.version = None

    def set_version(self, version: str):
        """set version"""
        self.version = str(version)

    @staticmethod
    def all_version() -> list:
        """get all version from minecraft server"""
        return utils.get_version_list()

    @staticmethod
    def all_alpha_version() -> list:
        """get all alpha version from minecraft server"""
        return [ide["id"] for ide in utils.get_version_list() if ide["type"] == "old_alpha"]

    @staticmethod
    def all_beta_version() -> list:
        """get all beta version from minecraft server"""
        return [ide["id"] for ide in utils.get_version_list() if ide["type"] == "old_beta"]

    @staticmethod
    def all_snapshot_version() -> list:
        """get all snapshot version from minecraft server"""
        return [ide["id"] for ide in utils.get_version_list() if ide["type"] == "snapshot"]

    @staticmethod
    def all_release_version() -> list:
        """get all release version from minecraft server"""
        return [ide["id"] for ide in utils.get_version_list() if ide["type"] == "release"]

    def all_installed_version(self) -> list:
        """get all installed version from minecraft folder"""
        return os.listdir(os.path.join(self.MinecraftFolder, "versions"))
