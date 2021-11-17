from .MM1_Lib import encode
import os
import random
from .Mcl_lib import account
from .Lang import lang


class ProfileLib:
    """Profile Library for Micrate Launcher

    :param str profile_folder: folder where profile was save
    :param str settings_folder: folder where settings was save
    """
    def __init__(self, profile_folder, settings_folder):
        self.folders = profile_folder
        if not os.path.isfile(os.path.join(settings_folder, "table.tbl")):
            encode.create_encode(random.randint(4, 20), os.path.join(settings_folder, "table.tbl"))
        self.encoder = encode.Encoder(os.path.join(settings_folder, "table.tbl"))

    def allProfile(self):
        """Get all profile

        :return dict: keys is profile id, value is username
        """
        profile = {}
        for i in os.listdir(self.folders):
            profile[i.split(".")[0]] = self.encoder.decode_str(
                self.encoder.encode_split(open(os.path.join(self.folders, i)).read())[0])
        return profile

    def createProfile(self, user, password):
        """Add profile

        :param user: minecraft username
        :param password: minecraft password
        :return:
        """
        connection = account.login_user(user, password)
        try:
            var = connection["error"]
            return ["NameError", connection["error"] + ": " + connection["errorMessage"]]
        except KeyError:
            test_slot = 0
            for Slots in range(20):
                if not os.path.exists(os.path.join(self.folders, str(Slots) + ".dat")):
                    with open(os.path.join(self.folders, str(Slots) + ".dat"), "w") as f:
                        f.write(self.encoder.encode_join(self.encoder.encode_str(connection["selectedProfile"]["name"]),
                                                         self.encoder.encode_str(user),
                                                         self.encoder.encode_str(password)))
                    self.setProfile(str(Slots))
                    test_slot = 1
                    break
            if test_slot == 0:
                return ["FileExistsError", lang["Text"]["Error"][2]]

    def deleteProfile(self, number):
        """delete profile with profile id

        :param number: profile id
        :return:
        """
        if os.path.exists(os.path.join(self.folders, str(number) + ".dat")):
            os.remove(os.path.join(self.folders, str(number) + ".dat"))
        else:
            return ["NameError", lang["Text"]["Error"][3]]

    def setProfile(self, number):
        """set profile with profile id

        :param number: profile id
        :return:
        """
        if os.path.exists(os.path.join(self.folders, str(number) + ".dat")):
            with open(os.path.join(self.folders, str(number) + ".dat")) as f:
                decoded = self.encoder.encode_split(f.read())
                connection = account.login_user(self.encoder.decode_str(decoded[1]),
                                                self.encoder.decode_str(decoded[2]))
            try:
                var = connection["error"]
                return ["NameError", connection["error"] + ": " + connection["errorMessage"]]
            except KeyError:
                self.login_data = connection
        else:
            return ["NameError", lang[26]]

    def changeSkin(self, skin, username):
        """change user skin

        :param skin: file path
        :param username: username
        :return:
        """
        if username == self.login_data['selectedProfile']['name']:
            if skin != '':
                account.upload_skin(self.login_data['selectedProfile']['id'], self.login_data['accessToken'], skin)
        else:
            return ["NameError", lang["Text"]["Error"][4]]
