import argparse

from generator.FacetModel.facet_model_generator import FacetModelGenerator
from generator.QuickViewsModel.quick_view_extractor import QuickViewExtractor
from generator.TfidfModel.tfidf_model_generator import TfidfModelGenerator
from generator.WordCountModel.word_count_model_generator import WordCountModelGenerator

FacetModelGenerator_inst = FacetModelGenerator()
WordCountModelGenerator_inst = WordCountModelGenerator()
TfidfGenerator_inst = TfidfModelGenerator()
QuickViewExtractor_inst = QuickViewExtractor()


def main():
    program_arguments = get_program_arguments()
    generate = program_arguments.generate
    is_generate_all = program_arguments.generate_all
    is_verbose = program_arguments.verbose

    print(generate)
    print(is_generate_all)
    print(is_verbose)


def get_program_arguments():
    arguments_parser = argparse.ArgumentParser(description='Whisper model generator.')
    arguments_parser.add_argument(
        '-g', '--generate',
        action='store',
        help='Specify which model to generate, can be multiple. a: analytics, f: facets, k: kmeans, t: tfidf, w: wordcount',
    )
    arguments_parser.add_argument(
        '-a', '--generate-all',
        action='store_true',
        help='Generate all models',
    )
    arguments_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print more information',
    )
    return arguments_parser.parse_args()

if __name__ == '__main__':
    main()
    #test = FacetModelGenerator_inst.generate_model()
    #t = QuickViewExtractor_inst.create_model()
    #WordCountModelGenerator_inst.generate_model(t)
    #TfidfGenerator_inst.generate_model(t)

    #bin_file = open('count_vectorizer_model.bin', 'rb')
    #x1 = pickle.load(bin_file)
    #bin_file.close()

    #bin_file = open('query_model.bin', 'rb')
    #x2 = pickle.load(bin_file)
    #bin_file.close()

    print('Test')
