import os
import configparser
from tkinter import simpledialog

CONFIG_FILE = "config.ini"

def get_api_key():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        return prompt_for_api_key(config)
    else:
        config.read(CONFIG_FILE)
        if 'DEFAULT' in config and 'OpenAIAPIKey' in config['DEFAULT']:
            return config['DEFAULT']['OpenAIAPIKey']
        else:
            return prompt_for_api_key(config)

def prompt_for_api_key(config):
    api_key = simpledialog.askstring("API Key", "Por favor, introduce tu clave de API de OpenAI:")
    if api_key:
        config['DEFAULT'] = {'OpenAIAPIKey': api_key}
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        return api_key
    else:
        return None

def reset_api_key():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    return get_api_key()