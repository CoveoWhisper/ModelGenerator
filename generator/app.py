import pickle

from definitions import Definitions
from generator.FacetModel.facet_model_generator import FacetModelGenerator
from generator.WordCountModel.word_count_model_generator import WordCountModelGenerator

FacetModelGenerator_inst = FacetModelGenerator()
WordCountModelGenerator_inst = WordCountModelGenerator()

if __name__ == '__main__':
    #test = FacetModelGenerator_inst.generate_model()
    #test = WordCountModelGenerator_inst.generate_model()

    print('Test')
