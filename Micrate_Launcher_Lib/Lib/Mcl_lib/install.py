from .natives import extract_natives_file, get_natives
from .helper import parseRuleList, inherit_json
from .utils import get_library_version
import requests
import shutil
import json
import os


def empty(arg):
    pass


def download_file(url, path, callback):
    if os.path.isfile(path):
        return
    try:
        os.makedirs(os.path.dirname(path))
    except:
        pass
    callback.get("setStatus", empty)("Download " + os.path.basename(path))
    r = requests.get(url, stream=True, headers={"user-agent": "minecraft-launcher-lib/" + get_library_version()})
    if r.status_code != 200:
        return False
    with open(path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
    return True


def install_libraries(data, path, callback):
    callback.get("setMax", empty)(len(data["libraries"]))
    for count, i in enumerate(data["libraries"]):
        # Check, if the rules allow this lib for the current system
        if not parseRuleList(i, "rules", {}):
            continue
        # Turn the name into a path
        current_path = os.path.join(path, "libraries")
        download_url = "https://libraries.minecraft.net"
        lib_path, name, version = i["name"].split(":")
        for libraries in lib_path.split("."):
            current_path = os.path.join(current_path, libraries)
            download_url = download_url + "/" + libraries
        download_url = download_url + "/" + name + "/" + version
        current_path = os.path.join(current_path, name, version)
        native = get_natives(i)
        # Check if there is a native file
        if native != "":
            jar_filename_native = name + "-" + version + "-" + native + ".jar"
        jar_filename = name + "-" + version + ".jar"
        download_url = download_url + "/" + jar_filename
        # Try to download the lib
        try:
            download_file(download_url, os.path.join(current_path, jar_filename), callback)
        except:
            pass
        if "downloads" not in i:
            if "extract" in i:
                extract_natives_file(os.path.join(current_path, jar_filename_native),
                                     os.path.join(path, "versions", data["id"], "natives"), i["extract"])
            continue
        if "artifact" in i["downloads"]:
            download_file(i["downloads"]["artifact"]["url"], os.path.join(current_path, jar_filename), callback)
        if native != "":
            download_file(i["downloads"]["classifiers"][native]["url"], os.path.join(current_path, jar_filename_native),
                          callback)
            if "extract" in i:
                extract_natives_file(os.path.join(current_path, jar_filename_native),
                                     os.path.join(path, "versions", data["id"], "natives"), i["extract"])
        callback.get("setProgress", empty)(count)


def install_assets(data, path, callback):
    # Old versions doesn't have this
    if "assetIndex" not in data:
        return
    # Download all assets
    download_file(data["assetIndex"]["url"], os.path.join(path, "assets", "indexes", data["assets"] + ".json"),
                  callback)
    with open(os.path.join(path, "assets", "indexes", data["assets"] + ".json")) as f:
        assets_data = json.load(f)
    # The assets gas a hash. e.g. c4dbabc820f04ba685694c63359429b22e3a62b5
    # With this hash, it can be download from
    # https://resources.download.minecraft.net/c4/c4dbabc820f04ba685694c63359429b22e3a62b5
    # And saved at assets/objects/c4/c4dbabc820f04ba685694c63359429b22e3a62b5
    callback.get("setMax", empty)(len(assets_data["objects"]))
    count = 0
    for key, value in assets_data["objects"].items():
        download_file("https://resources.download.minecraft.net/" + value["hash"][:2] + "/" + value["hash"],
                      os.path.join(path, "assets", "objects", value["hash"][:2], value["hash"]), callback)
        count += 1
        callback.get("setProgress", empty)(count)


def do_version_install(version_id, path, callback, url=None):
    # Download and read versions.json
    if url:
        download_file(url, os.path.join(path, "versions", version_id, version_id + ".json"), callback)
    with open(os.path.join(path, "versions", version_id, version_id + ".json")) as f:
        version_data = json.load(f)
    # For Forge
    if "inheritsFrom" in version_data:
        version_data = inherit_json(version_data, path)
    install_libraries(version_data, path, callback)
    install_assets(version_data, path, callback)
    # Download minecraft.jar
    if "downloads" in version_data:
        download_file(version_data["downloads"]["client"]["url"],
                      os.path.join(path, "versions", version_data["id"], version_data["id"] + ".jar"), callback)
    # Need to copy jar for old forge versions
    if not os.path.isfile(os.path.join(path, "versions", version_data["id"],
                                       version_data["id"] + ".jar")) and "inheritsFrom" in version_data:
        inherits_from = version_data["inheritsFrom"]
        shutil.copyfile(os.path.join(path, "versions", version_data["id"], version_data["id"] + ".jar"),
                        os.path.join(path, "versions", inherits_from, inherits_from + ".jar"))


def install_minecraft_version(version_id, path, callback=None):
    if callback is None:
        callback = {}
    version_list = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
    for i in version_list["versions"]:
        if i["id"] == version_id:
            do_version_install(version_id, path, callback, url=i["url"])
            return True
    if not os.path.isdir(os.path.join(path, "versions")):
        return False
    for i in os.listdir(os.path.join(path, "versions")):
        if i == version_id:
            do_version_install(version_id, path, callback)
            return True
    return False
