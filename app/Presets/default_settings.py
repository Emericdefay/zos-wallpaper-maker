import json


def load_settings():
    """
        Charge les paramètres à partir d'un fichier json. Si le 
        fichier n'existe pas, il est créé à partir des paramètres par défaut.
    """
    # Vérification de l'existence de "settings.json"
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
    except Exception:
        # Création de "settings.json" à partir des paramètres par défaut
        with open("settings.json", "w") as f:
            json.dump(write_default_json(), f, indent=4)
        with open("settings.json", "r") as f:
            settings = json.load(f)
    return settings


def write_default_json():
    return json.loads('''{
    "DISPLAYED_COLORS": [
        "0x000000",
        "0x2986cc",
        "0xcc0000",
        "0xc90076",
        "0x8fce00",
        "0x6a329f",
        "0xffe200",
        "0xffffff"
    ],
    "PREVIEWED_COLORS": [
        "0x000000",
        "0x00ffff",
        "0xff0000",
        "0xffa0a0",
        "0x00ff00",
        "0x6ebbff",
        "0xffff00",
        "0xffffff"
    ],
    "ASSOCIATED_NAME": [
        "BLACK",
        "BLUE",
        "RED",
        "PINK",
        "GREEN",
        "PURPLE",
        "YELLOW",
        "WHITE" 
    ]
}''')
