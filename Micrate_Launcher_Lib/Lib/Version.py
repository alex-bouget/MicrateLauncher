from .Mcl_lib import utils
import os


class VersionLib:
    def __init__(self, minecraft_folder):
        self.MinecraftFolder = minecraft_folder
        self.version = None

    def setVersion(self, version):
        self.version = str(version)

    @staticmethod
    def allVersion():
        return utils.get_version_list()

    @staticmethod
    def allAlphaVersion():
        return [ide["id"] for ide in utils.get_version_list() if ide["type"] == "old_alpha"]

    @staticmethod
    def allBetaVersion():
        return [ide["id"] for ide in utils.get_version_list() if ide["type"] == "old_beta"]

    @staticmethod
    def allSnapshotVersion():
        return [ide["id"] for ide in utils.get_version_list() if ide["type"] == "snapshot"]

    @staticmethod
    def allReleaseVersion():
        return [ide["id"] for ide in utils.get_version_list() if ide["type"] == "release"]

    def allInstalledVersion(self):
        return os.listdir(os.path.join(self.MinecraftFolder, "versions"))
