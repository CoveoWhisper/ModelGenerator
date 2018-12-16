import os

import json

from definitions import Definitions
from generator.AnalyticsModel.analysis import get_search_to_clicks_mapping
from generator.AnalyticsModel.clicks_counts import get_clicks_counts
from generator.AnalyticsModel.history import get_history

SEARCHES_FILE_PATH = "data/searches.csv"
CLICKS_FILE_PATH = "data/clicks.csv"
DOCUMENTS_POPULARITY_PATH = "output/documents_popularity.json"
DOCUMENTS_SEARCHES_MAPPING_PATH = "output/documents_searches_mapping.json"


class AnalyticsModelGenerator(object):

    def generate_model(self, is_verbose):
        if is_verbose:
            print('-- ANALYTICS MODEL GENERATOR STARTED --')
            print('Generating popularity document')
        pop = self.generate_documents_popularity(CLICKS_FILE_PATH, is_verbose)
        if is_verbose:
            print('-- Generating searches document--')
        searches = self.generate_documents_searches_mapping(SEARCHES_FILE_PATH, CLICKS_FILE_PATH, is_verbose)
        if is_verbose:
            print('-- Saving clicks.csv--')
        self.save_model(pop, Definitions.ROOT_DIR + DOCUMENTS_POPULARITY_PATH)
        if is_verbose:
            print('-- Saving searches.csv--')
        self.save_model(searches, Definitions.ROOT_DIR + DOCUMENTS_SEARCHES_MAPPING_PATH)
        if is_verbose:
            print('-- ANALYTICS MODEL GENERATOR ENDED --')

    @staticmethod
    def generate_documents_popularity(path, is_verbose):
        return get_clicks_counts(path, is_verbose)

    @staticmethod
    def generate_documents_searches_mapping(searches_file_path, clicks_file_path, is_verbose):
        if is_verbose:
            print('Gettting history of document in analytics files')
        history = get_history(searches_file_path, clicks_file_path)
        documents_searches_mapping = get_search_to_clicks_mapping(history)
        for documents_search_mapping in documents_searches_mapping:
            documents_searches_mapping[documents_search_mapping] = \
                list(documents_searches_mapping[documents_search_mapping])

        return documents_searches_mapping

    @staticmethod
    def save_model(model, save_path):
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as out_file:
            json.dump(model, out_file, sort_keys=True, indent=4)
