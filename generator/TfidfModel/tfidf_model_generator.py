import pandas as pd
import pickle
from pathlib import Path

import json
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from definitions import Definitions


class TfidfModelGenerator(object):

    def generate_model(self, model):
        tfidf_vectorizer = self.vectorize(model)
        self.save_model(tfidf_vectorizer, Definitions.ROOT_DIR)

    @staticmethod
    def vectorize(model):
        tfidf_vectorizer = TfidfVectorizer()
        return pd.DataFrame(tfidf_vectorizer.fit_transform(model).toarray(),
                                  columns=tfidf_vectorizer.get_feature_names(), index=None)

    @staticmethod
    def save_model(model, save_path):
        with open(save_path + '/query_model.bin', 'wb') as bin_file:
            pickle.dump(model, bin_file)
