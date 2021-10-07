import os


def create_dir_tree(path):
    path_cut = os.path.normpath(path).split('\\')
    for i in range(len(path_cut)):
        all_dir = []
        for o in range(i+1):
            all_dir.append(path_cut[o])
        try:
            os.mkdir(os.path.join(*all_dir))
        except FileExistsError:
            pass


class SuperFolders:
    def __init__(self):
        self.folders_name = []
        self.folders = []

    def add_folder(self, name, directory):
        if os.path.exists(directory):
            if name in self.folders_name:
                raise NameError("folder name already created")
            else:
                self.folders_name.append(name)
                self.folders.append(directory)
        else:
            create_dir_tree(directory)
            self.add_folder(name, directory)

    def del_folder(self, name):
        if name in self.folders_name:
            del self.folders[self.folders_name.index(name)]
            del self.folders_name[self.folders_name.index(name)]
        else:
            raise NameError("folder name not created")

    def get_folder(self, name):
        return self.folders[self.folders_name.index(name)]

    def set_folder(self, name, folder):
        if name in self.folders_name:
            if os.path.exists(folder):
                self.folders[self.folders_name.index(name)] = folder
            else:
                create_dir_tree(folder)
                self.set_folder(name, folder)
        else:
            raise NameError("folder name not created")
