import pandas as pd
import pickle
from pathlib import Path

import json
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from definitions import Definitions


class TfIdfModelGenerator(object):

    def generate_model(self, model, is_verbose):
        if is_verbose:
            print('-- TFIDF MODEL GENERATOR STARTED --')
            print('vectorizing model')
        tf_idf_vectorizer = self.vectorize(model)
        if is_verbose:
            print('saving query_model.bin')
        self.save_model(tf_idf_vectorizer, Definitions.ROOT_DIR + '/output/query_model.bin', 'wb')
        if is_verbose:
            print('-- TFIDF MODEL GENERATOR  ENDED --')

    @staticmethod
    def vectorize(model):
        tf_idf_vectorizer = TfidfVectorizer()
        return pd.DataFrame(tf_idf_vectorizer.fit_transform(model).toarray(),
                                  columns=tf_idf_vectorizer.get_feature_names(), index=None)

    @staticmethod
    def save_model(model, save_path):
        with open(save_path) as bin_file:
            pickle.dump(model, bin_file)
