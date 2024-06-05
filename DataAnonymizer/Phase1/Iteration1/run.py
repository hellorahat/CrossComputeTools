import json
from sys import argv
from os.path import join

input_folder, output_folder = argv[1:]

class input_processor_class:
    def __init__(self):
        self.input_path = join(input_folder, "input.csv")
        
        with open(join(input_folder, "variables.dictionary")) as f:
            data = json.load(f)
            self.generalization_number_columns = data["generalization_number_columns"]
            self.generalization_location_columns = data["generalization_location_columns"]
            self.suppression_columns = data["suppression_columns"]
            self.words_to_suppress = data["words_to_suppress"]
            
    
class output_processor_class:
    def __init__(self):
        pass
    
input_processor = input_processor_class()
print(input_processor.suppression_columns)