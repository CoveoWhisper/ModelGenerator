import pickle

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from definitions import Definitions


class KMeansModelGenerator(object):

    def generate_model(self, model, is_verbose):
        if is_verbose:
            print('-- KMEANS MODEL GENERATOR STARTED --')
        tf_idf_vectorizer, tf_idf_matrix = self.vectorize(model, is_verbose)

        if is_verbose:
            print('saving tf_idf_vectorizer.bin')
        self.save_model(tf_idf_vectorizer, Definitions.ROOT_DIR + '/output/tf_idf_vectorizer.bin')
        if is_verbose:
            print('saving k_means_clustering_model.bin')
        self.save_model(tf_idf_matrix, Definitions.ROOT_DIR + '/output/k_means_clustering_model.bin')
        if is_verbose:
            print('-- KMEANS MODEL GENERATOR ENDED --')

    @staticmethod
    def vectorize(model, is_verbose):

        num_clusters = 10
        max_iterations = 300

        # create k-means model
        clustering_model = KMeans(
            n_clusters=num_clusters,
            max_iter=max_iterations,
            precompute_distances="auto",
            n_jobs=-1
        )

        if is_verbose:
            print('vectorizing model')
        tf_idf_vectorizer = TfidfVectorizer(analyzer="word", use_idf=True, smooth_idf=True, ngram_range=(2, 3))
        tf_idf_matrix = tf_idf_vectorizer.fit_transform(model)
        if is_verbose:
            print('clustering model')
        clustering_model_result = clustering_model.fit(tf_idf_matrix)

        return tf_idf_vectorizer, clustering_model_result

    @staticmethod
    def save_model(model, file_name):
        with open(file_name, 'wb') as bin_file:
            pickle.dump(model, bin_file)
