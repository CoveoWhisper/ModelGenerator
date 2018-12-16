import pandas as pd
import pickle
from pathlib import Path

import json
from sklearn.feature_extraction.text import CountVectorizer

from definitions import Definitions


class WordCountModelGenerator(object):
    FILENAME = ''
    NUMBER_OF_RESULTS_PER_QUERY = 1000
    CREDENTIALS_PATH = Path(Definitions.ROOT_DIR + "/appsettings_secret.json")
    ATTRIBUTES_LIST = ['title', 'tags', 'concepts', 'documenttype', 'sourcetype', 'source', 'collection', 'filetype',
                       'sitename']
    LANGUAGE = 'english'
    RAW_LANGUAGE = 'English'

    def __init__(self):
        with open(self.CREDENTIALS_PATH, 'r') as file:
            values = json.load(file)
            self.search_URL = values['SearchURL']
            self.headers = {'Authorization': 'Bearer ' + values['ApiKey']}

    def generate_model(self, model):
        count_vectorizer = self.vectorize(model)
        self.save_model(count_vectorizer, Definitions.ROOT_DIR)

    @staticmethod
    def vectorize(model):
        count_vectorizer = CountVectorizer()
        return pd.DataFrame(count_vectorizer.fit_transform(model).toarray(),
                            columns=count_vectorizer.get_feature_names(), index=None)

    @staticmethod
    def save_model(model, save_path):
        with open(save_path + '/count_vectorizer_model.bin', 'wb') as bin_file:
            pickle.dump(model, bin_file)
