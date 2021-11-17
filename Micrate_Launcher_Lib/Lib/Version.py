from .Mcl_lib import utils
import os


class VersionLib:
    """Minecraft Version library
    get all version and all installed version

    :param str minecraft_folder: folder where minecraft was downloaded
    """
    def __init__(self, minecraft_folder):
        self.MinecraftFolder = minecraft_folder
        self.version = None

    def setVersion(self, version):
        """set version

        :param version:
        :return:
        """
        self.version = str(version)

    @staticmethod
    def allVersion():
        """get all version from minecraft server

        :return list:
        """
        return utils.get_version_list()

    @staticmethod
    def allAlphaVersion():
        """get all alpha version from minecraft server

        :return list:
        """
        return [ide["id"] for ide in utils.get_version_list() if ide["type"] == "old_alpha"]

    @staticmethod
    def allBetaVersion():
        """get all beta version from minecraft server

        :return list:
        """
        return [ide["id"] for ide in utils.get_version_list() if ide["type"] == "old_beta"]

    @staticmethod
    def allSnapshotVersion():
        """get all snapshot version from minecraft server

        :return list:
        """
        return [ide["id"] for ide in utils.get_version_list() if ide["type"] == "snapshot"]

    @staticmethod
    def allReleaseVersion():
        """get all release version from minecraft server

        :return list:
        """
        return [ide["id"] for ide in utils.get_version_list() if ide["type"] == "release"]

    def allInstalledVersion(self):
        """get all installed version from minecraft folder

        :return list:
        """
        return os.listdir(os.path.join(self.MinecraftFolder, "versions"))
