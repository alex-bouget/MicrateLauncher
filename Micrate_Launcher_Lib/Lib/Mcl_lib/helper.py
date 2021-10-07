import platform
import json
import os


def parseSingeRule(rule, options):
    # Parse a rule from the versions.json
    return_value = True
    if rule["action"] == "allow":
        return_value = False
    elif rule["action"] == "disallow":
        return_value = True
    if "os" in rule:
        for key, value in rule["os"].items():
            if key == "name":
                if value == "windows" and platform.system() != 'Windows':
                    return return_value
                elif value == "osx" and platform.system() != 'Darwin':
                    return return_value
                elif value == "linux" and platform.system() != 'Linux':
                    return return_value
            elif key == "arch":
                if value == "x86" and platform.architecture()[0] != "32bit":
                    return return_value
    if "features" in rule:
        for key, value in rule["features"].items():
            if key == "has_custom_resolution" and not options.get("customResolution", False):
                return return_value
            elif key == "is_demo_user" and not options.get("demo", False):
                return return_value
    return not return_value


def parseRuleList(data, rule_string, options):
    # Parse a rule list
    if rule_string not in data:
        return True
    for i in data[rule_string]:
        if not parseSingeRule(i, options):
            return False
    return True


def getNatives(data):
    if platform.architecture()[0] == "32bit":
        arch_type = "32"
    else:
        arch_type = "64"
    if "natives" in data:
        if platform.system() == 'Windows':
            if "windows" in data["natives"]:
                return data["natives"]["windows"].replace("${arch}", arch_type)
            else:
                return ""
        elif platform.system() == 'Darwin':
            if "osx" in data["natives"]:
                return data["natives"]["osx"].replace("${arch}", arch_type)
            else:
                return ""
        else:
            if "linux" in data["natives"]:
                return data["natives"]["linux"].replace("${arch}", arch_type)
            else:
                return ""
    else:
        return ""


def inherit_json(original_data, path):
    # See https://github.com/tomsik68/mclauncher-api/wiki/Version-Inheritance-&-Forge
    inherit_version = original_data["inheritsFrom"]
    with open(os.path.join(path, "versions", inherit_version, inherit_version + ".json")) as f:
        new_data = json.load(f)
    for key, value in original_data.items():
        if isinstance(value, list) and isinstance(new_data.get(key, None), list):
            new_data[key] = value + new_data[key]
        elif isinstance(value, dict) and isinstance(new_data.get(key, None), dict):
            for a, b in value.items():
                if isinstance(b, list):
                    new_data[key][a] = new_data[key][a] + b
        else:
            if key != "id":
                new_data[key] = value
    return new_data
