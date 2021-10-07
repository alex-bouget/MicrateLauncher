from .helper import parseRuleList, inherit_json
from .utils import get_library_version
from .natives import get_natives
import platform
import json
import copy
import os


def get_libraries(data, path):
    if platform.system() == "Windows":
        classpath_separator = ";"
    else:
        classpath_separator = ":"
    lib_string = ""
    for i in data["libraries"]:
        if not parseRuleList(i, "rules", {}):
            continue
        current_path = os.path.join(path, "libraries")
        lib_path, name, version = i["name"].split(":")
        for libraries in lib_path.split("."):
            current_path = os.path.join(current_path, libraries)
        current_path = os.path.join(current_path, name, version)
        native = get_natives(i)
        if native == "":
            jar_filename = name + "-" + version + ".jar"
        else:
            jar_filename = name + "-" + version + "-" + native + ".jar"
        current_path = os.path.join(current_path, jar_filename)
        lib_string = lib_string + current_path + classpath_separator
    if "jar" in data:
        lib_string = lib_string + os.path.join(path, "versions", data["jar"], data["jar"] + ".jar")
    else:
        lib_string = lib_string + os.path.join(path, "versions", data["id"], data["id"] + ".jar")
    return lib_string


def replace_arguments(arg_string, version_data, path, options):
    # Replace all arguments with the needed value
    arg_string = arg_string.replace("${natives_directory}", options["nativesDirectory"])
    arg_string = arg_string.replace("${launcher_name}", options.get("launcherName", "minecraft-launcher-lib"))
    arg_string = arg_string.replace("${launcher_version}", options.get("launcherVersion", get_library_version()))
    arg_string = arg_string.replace("${classpath}", options["classpath"])
    arg_string = arg_string.replace("${auth_player_name}", options.get("username", "{username}"))
    arg_string = arg_string.replace("${version_name}", version_data["id"])
    arg_string = arg_string.replace("${game_directory}", options.get("gameDirectory", path))
    arg_string = arg_string.replace("${assets_root}", os.path.join(path, "assets"))
    arg_string = arg_string.replace("${assets_index_name}", version_data.get("assets", version_data["id"]))
    arg_string = arg_string.replace("${auth_uuid}", options.get("uuid", "{uuid}"))
    arg_string = arg_string.replace("${auth_access_token}", options.get("token", "{token}"))
    arg_string = arg_string.replace("${user_type}", "mojang")
    arg_string = arg_string.replace("${version_type}", version_data["type"])
    arg_string = arg_string.replace("${user_properties}", "{}")
    arg_string = arg_string.replace("${resolution_width}", options.get("resolutionWidth", "854"))
    arg_string = arg_string.replace("${resolution_height}", options.get("resolutionHeight", "480"))
    arg_string = arg_string.replace("${game_assets}", os.path.join(path, "assets", "virtual", "legacy"))
    arg_string = arg_string.replace("${auth_session}", options.get("token", "{token}"))
    return arg_string


def get_arguments_string(version_data, path, options):
    arg_list = []
    for v in version_data["minecraftArguments"].split(" "):
        v = replace_arguments(v, version_data, path, options)
        arg_list.append(v)
    # Custom resolution is not in the list
    if options.get("customResolution", False):
        arg_list.append("--width")
        arg_list.append(options.get("resolutionWidth", "854"))
        arg_list.append("--height")
        arg_list.append(options.get("resolutionHeight", "480"))
    if options.get("demo", False):
        arg_list.append("--demo")
    return arg_list


def get_arguments(data, version_data, path, options):
    arg_list = []
    for i in data:
        # Rules might has 2 different names in different versions.json
        if not parseRuleList(i, "compatibilityRules", options):
            continue
        if not parseRuleList(i, "rules", options):
            continue
        # i could be the argument
        if isinstance(i, str):
            arg_list.append(replace_arguments(i, version_data, path, options))
        else:
            # Sometimes  i["value"] is the argument
            if isinstance(i["value"], str):
                arg_list.append(replace_arguments(i["value"], version_data, path, options))
            # Sometimes i["value"] is a list of arguments
            else:
                for v in i["value"]:
                    v = replace_arguments(v, version_data, path, options)
                    arg_list.append(v)
    return arg_list


def get_minecraft_command(version, path, options):
    options = copy.copy(options)
    with open(os.path.join(path, "versions", version, version + ".json")) as f:
        data = json.load(f)
    if "inheritsFrom" in data:
        data = inherit_json(data, path)
    options["nativesDirectory"] = options.get("nativesDirectory", os.path.join(path, "versions", data["id"], "natives"))
    options["classpath"] = get_libraries(data, path)
    command = [options.get("executablePath", "java")]
    if "jvmArguments" in options:
        command = command + options["jvmArguments"]
    # Newer Versions have jvmArguments in version.json
    if isinstance(data.get("arguments", None), dict):
        if "jvm" in data["arguments"]:
            command = command + get_arguments(data["arguments"]["jvm"], data, path, options)
        else:
            command.append("-Djava.library.path=" + options["nativesDirectory"])
            command.append("-cp")
            command.append(options["classpath"])
    else:
        command.append("-Djava.library.path=" + options["nativesDirectory"])
        command.append("-cp")
        command.append(options["classpath"])
    command.append(data["mainClass"])
    if "minecraftArguments" in data:
        # For older versions
        command = command + get_arguments_string(data, path, options)
    else:
        command = command + get_arguments(data["arguments"]["game"], data, path, options)
    if "server" in options:
        command.append("--server")
        command.append(options["server"])
        if "port" in options:
            command.append("--port")
            command.append(options["port"])
    return command
