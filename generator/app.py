from generator.FacetModel.facet_model_generator import FacetModelGenerator

FacetModelGenerator_inst = FacetModelGenerator()

if __name__ == '__main__':
    test = FacetModelGenerator_inst.generate_model()
    print('Test')
