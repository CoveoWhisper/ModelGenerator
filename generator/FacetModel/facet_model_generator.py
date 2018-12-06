import json
from definitions import Definitions
from pathlib import Path


class FacetModelGenerator(object):
    CREDENTIALS_PATH = Path(Definitions.ROOT_DIR + "/appsettings_secret.json")

    def __init__(self):
        with open(FacetModelGenerator.CREDENTIALS_PATH, 'r') as file:
            values = json.load(file)
            self.ApiKey = values['ApiKey']
            self.SearchBaseAddress = values['SearchBaseAddress']

    def generate_model(self):
        return ''
