from generator.FacetModel.facet_model_generator import FacetModelGenerator

FacetModelGenerator_inst = FacetModelGenerator()

if __name__ == '__main__':
    test = FacetModelGenerator_inst.get_all_documents_for_all_facets()
    print('Test')
