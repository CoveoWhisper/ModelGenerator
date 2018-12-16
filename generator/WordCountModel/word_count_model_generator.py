import pickle
from pathlib import Path

import requests
import json
from nltk import word_tokenize, re

from definitions import Definitions
from generator.WordCountModel.HTMLExtractor import HTMLExtractor
from generator.WordCountModel.WordModel import WordModel


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

    def generate_model(self):
        model = self.create_model()
        self.save_model(model, Definitions.ROOT_DIR)

    def create_model(self):
        smaller_id = 0
        model = WordModel()
        factory = HTMLExtractor()
        data = {'numberOfResults': str(self.NUMBER_OF_RESULTS_PER_QUERY), 'sortCriteria': '@rowid ascending', 'cq': ''}
        
        while True:
            data['cq'] = '@rowid>' + str(smaller_id)
            response = requests.post(self.search_URL, headers=self.headers, data=data).json()

            if response["totalCount"] == 0:
                break

            smaller_id = response['results'][-1]['raw']['rowid']
            for result in response['results']:
                if 'language' not in result['raw'] or self.RAW_LANGUAGE not in result['raw']['language']:
                    continue

                model.add_words(self.parseResult(result))
                url = 'https://cloudplatform.coveo.com/rest/search/v2/html?uniqueId=' + result['UniqueId']

                extracted_text = factory.extract_from_file_path(url, self.headers)
                words = self.parseText(extracted_text)
                model.add_words(words)

        return model

    @staticmethod
    def save_model(model, save_path):
        with open(save_path + '/WordCount.bin', 'wb') as bin_file:
            pickle.dump(model, bin_file)

    @staticmethod
    def parseResult(result):
        raw = result['raw']
        words = []
        for attribute in WordCountModelGenerator.ATTRIBUTES_LIST:
            if attribute not in raw:
                continue

            item = raw[attribute]
            if isinstance(item, list):
                for x in item:
                    words += word_tokenize(x, language=WordCountModelGenerator.LANGUAGE)
            else:
                words += word_tokenize(item, language=WordCountModelGenerator.LANGUAGE)

        regex = re.compile('[^a-zA-Z0-9]')
        words = [regex.sub('', w).lower() for w in words]
        words = [w for w in words if w]

        return words

    @staticmethod
    def parseText(text):
        words = word_tokenize(text, language=WordCountModelGenerator.LANGUAGE)

        regex = re.compile('[^a-zA-Z0-9]')
        words = [regex.sub('', w).lower() for w in words]
        words = [w for w in words if w]

        return words
