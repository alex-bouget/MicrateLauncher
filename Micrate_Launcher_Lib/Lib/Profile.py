from .MM1_Lib import encode
import os
import random
from .Mcl_lib import account
from ..Lang import lang


"""Library for the Profile"""


class ProfileLib:
    folders: str
    """folder where profile was saved"""
    encode: encode.Encoder
    """encoder of the profile"""
    login_data: dict

    def __init__(self, profile_folder: str, settings_folder: str):
        """Constructor"""
        self.folders = profile_folder
        if not os.path.isfile(os.path.join(settings_folder, "table.tbl")):
            encode.create_encode(random.randint(4, 20), os.path.join(settings_folder, "table.tbl"))
        self.encoder = encode.Encoder(os.path.join(settings_folder, "table.tbl"))

    def all_profile(self) -> dict:
        """Get all profile"""
        profile = {}
        for i in os.listdir(self.folders):
            profile[i.split(".")[0]] = self.encoder.decode_str(
                self.encoder.encode_split(open(os.path.join(self.folders, i)).read())[0])
        return profile

    def create_profile(self, user: str, password: str):
        """Add profile"""
        connection = account.login_user(user, password)
        if "error" in connection.keys():
            return ["NameError", connection["error"] + ": " + connection["errorMessage"]]
        else:
            test_slot = 0
            for Slots in range(20):
                if not os.path.exists(os.path.join(self.folders, str(Slots) + ".dat")):
                    with open(os.path.join(self.folders, str(Slots) + ".dat"), "w") as f:
                        f.write(self.encoder.encode_join(self.encoder.encode_str(connection["selectedProfile"]["name"]),
                                                         self.encoder.encode_str(user),
                                                         self.encoder.encode_str(password)))
                    self.set_profile(Slots)
                    test_slot = 1
                    break
            if test_slot == 0:
                return ["FileExistsError", lang["Text"]["Error"][2]]

    def delete_profile(self, number: int):
        """delete profile with profile id"""
        if os.path.exists(os.path.join(self.folders, str(number) + ".dat")):
            os.remove(os.path.join(self.folders, str(number) + ".dat"))
        else:
            return ["NameError", lang["Text"]["Error"][3]]

    def set_profile(self, number: int):
        """set profile with profile id"""
        if os.path.exists(os.path.join(self.folders, str(number) + ".dat")):
            with open(os.path.join(self.folders, str(number) + ".dat")) as f:
                decoded = self.encoder.encode_split(f.read())
                connection = account.login_user(self.encoder.decode_str(decoded[1]),
                                                self.encoder.decode_str(decoded[2]))
            if "error" in connection.keys():
                return ["NameError", connection["error"] + ": " + connection["errorMessage"]]
            else:
                self.login_data = connection
        else:
            return ["NameError", lang[26]]

    def change_skin(self, skin: str, username: str):
        """change user skin"""
        if username == self.login_data['selectedProfile']['name']:
            if skin != '':
                account.upload_skin(self.login_data['selectedProfile']['id'], self.login_data['accessToken'], skin)
        else:
            return ["NameError", lang["Text"]["Error"][4]]
