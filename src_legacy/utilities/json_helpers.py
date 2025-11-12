import json

##########

LOCAL_CONFIG_PATH = "./local_config.json"


def save_config(config_object: dict, path: str = LOCAL_CONFIG_PATH):
    with open(path, "w") as out_:
        json.dump(config_object, out_)


def load_config(path: str = LOCAL_CONFIG_PATH) -> dict:
    with open(path) as in_:
        return json.load(in_)
