from pathlib import Path

import requests
import json
from nltk import word_tokenize, re

from definitions import Definitions
from generator.QuickViewsModel.HTMLExtractor import HTMLExtractor


class QuickViewExtractor(object):
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

    def create_model(self):
        smaller_id = 0
        model = []
        factory = HTMLExtractor()
        data = {'numberOfResults': str(self.NUMBER_OF_RESULTS_PER_QUERY), 'sortCriteria': '@rowid ascending', 'cq': ''}

        #i = 0
        while True:
            data['cq'] = '@rowid>' + str(smaller_id)
            response = requests.post(self.search_URL, headers=self.headers, data=data).json()

            if response["totalCount"] == 0:
                break

            smaller_id = response['results'][-1]['raw']['rowid']
            for result in response['results']:
                if 'language' not in result['raw'] or self.RAW_LANGUAGE not in result['raw']['language']:
                    continue

                url = 'https://cloudplatform.coveo.com/rest/search/v2/html?uniqueId=' + result['UniqueId']

                extracted_text = factory.extract_from_file_path(url, self.headers)
                words = ' '.join(self.parseText(extracted_text))
                model.append(words)

                #i += 1
                #if i > 10:
                 #   return model

        return model

    @staticmethod
    def parseText(text):
        words = word_tokenize(text, language=QuickViewExtractor.LANGUAGE)

        regex = re.compile('[^a-zA-Z0-9]')
        words = [regex.sub('', w).lower() for w in words]
        words = [w for w in words if w]

        return words
