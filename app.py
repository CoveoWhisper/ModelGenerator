import argparse

from generator.AnalyticsModel.analytics_model_generator import AnalyticsModelGenerator
from generator.FacetModel.facet_model_generator import FacetModelGenerator
from generator.KMeansModel.kmeans_model_generator import KMeansModelGenerator
from generator.QuickViewsModel.quick_view_extractor import QuickViewExtractor
from generator.TfidfModel.tfidf_model_generator import TfIdfModelGenerator
from generator.WordCountModel.word_count_model_generator import WordCountModelGenerator


def main():
    program_arguments = get_program_arguments()
    is_verbose = program_arguments.verbose

    if program_arguments.generate_all:
        FacetModelGenerator().generate_model()
        AnalyticsModelGenerator().generate_model(is_verbose)
        model = QuickViewExtractor().create_model(is_verbose)
        WordCountModelGenerator().generate_model(model, is_verbose)
        TfIdfModelGenerator().generate_model(model, is_verbose)
        KMeansModelGenerator().generate_model(model, is_verbose)

    else:
        generate = program_arguments.generate
        if 'a' in generate:
            AnalyticsModelGenerator().generate_model(is_verbose)
        if 'f' in generate:
            FacetModelGenerator().generate_model()
        if 't' or 'w' or 'k' in generate:
            model = QuickViewExtractor().create_model(is_verbose)
            if 't' in generate:
                TfIdfModelGenerator().generate_model(model, is_verbose)
            if 'w' in generate:
                WordCountModelGenerator().generate_model(model, is_verbose)
            if 'k' in generate:
                KMeansModelGenerator().generate_model(model, is_verbose)


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
