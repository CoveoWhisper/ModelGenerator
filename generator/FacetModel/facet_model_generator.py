import json
import requests
from definitions import Definitions
from pathlib import Path
from generator.FacetModel.Facet import Facet


class FacetModelGenerator(object):
    CREDENTIALS_PATH = Path(Definitions.ROOT_DIR + "/appsettings_secret.json")
    NUMBER_OF_RESULTS_PER_QUERY = 1000

    def __init__(self):
        with open(FacetModelGenerator.CREDENTIALS_PATH, 'r') as file:
            values = json.load(file)
            self.apiKey = values['ApiKey']
            self.get_fields_URL = values['GetFieldsURL']
            self.get_fields_value_URL = values['GetFieldsValueURL']
            self.search_URL = values['SearchURL']
            self.headers = {'Authorization': 'Bearer ' + self.apiKey}

    def generate_model(self):
        return ''

    def get_all_facets_name(self):
        response = requests.get(self.get_fields_URL, headers=self.headers).json()
        return [val['name'] for val in response['fields'] if val['groupByField'] is True]

    def get_all_facets(self):
        facets_name = self.get_all_facets_name()

        facets = dict()
        for facet_name in facets_name:
            data = {'field': facet_name}
            response = requests.post(self.get_fields_value_URL, headers=self.headers, data=data).json()
            values = [val['value'] for val in response['values']]
            facets[facet_name] = values

        return facets

    def get_all_documents_for_all_facets(self):
        facets = self.get_all_facets()

        facet_with_documents = dict()

        for name, values in facets.items():
            for value in values:
                if ',' in value:
                    continue

                rowId = 0
                number_result = 1
                data = {'numberOfResults': str(self.NUMBER_OF_RESULTS_PER_QUERY), 'sortCriteria': '@rowid ascending', 'aq': ''}
                documents_uri = list()
                while number_result != 0:
                    data['aq'] = name + '==' + value.replace(' -', '') + '* AND @rowId>' + str(rowId)
                    response = requests.post(self.search_URL, headers=self.headers, data=data).json()

                    number_result = response['totalCount']

                    if number_result != 0:
                        rowId = response['results'][-1]['raw']['rowid']
                        documents_uri.extend(document['uri'] for document in response['results'])

                facet_with_documents[Facet(name, value)] = documents_uri

        return facet_with_documents

