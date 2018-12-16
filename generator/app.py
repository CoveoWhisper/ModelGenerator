import pickle

from definitions import Definitions
from generator.FacetModel.facet_model_generator import FacetModelGenerator
from generator.QuickViewsModel.quick_view_extractor import QuickViewExtractor
from generator.WordCountModel.word_count_model_generator import WordCountModelGenerator

FacetModelGenerator_inst = FacetModelGenerator()
WordCountModelGenerator_inst = WordCountModelGenerator()
QuickViewExtractor_inst = QuickViewExtractor()

if __name__ == '__main__':
    #test = FacetModelGenerator_inst.generate_model()
    t = QuickViewExtractor_inst.create_model()
    WordCountModelGenerator_inst.generate_model(t)

    bin_file = open('count_vectorizer_model.bin', 'rb')
    uri_to_quickView = pickle.load(bin_file)
    bin_file.close()

    print('Test')
