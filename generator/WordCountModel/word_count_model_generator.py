import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer

from definitions import Definitions


class WordCountModelGenerator(object):

    def generate_model(self, model):
        count_vectorizer = self.vectorize(model)
        self.save_model(count_vectorizer, Definitions.ROOT_DIR + '/output/count_vectorizer_model.bin', 'wb')

    @staticmethod
    def vectorize(model):
        count_vectorizer = CountVectorizer()
        return pd.DataFrame(count_vectorizer.fit_transform(model).toarray(),
                            columns=count_vectorizer.get_feature_names(), index=None)

    @staticmethod
    def save_model(model, save_path):
        with open(save_path) as bin_file:
            pickle.dump(model, bin_file)
