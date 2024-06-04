import json
from sys import argv
from os.path import join

input_folder, output_folder = argv[1:]

class input_processor_class:
    def __init__(self):
        self.input_path = join(input_folder, "input.csv")
        
        self.generalization_number_columns = ""
        self.generalization_location_columns = ""
        self.suppression_columns = ""
        self.words_to_suppress = ""
    def processInputs():
        pass
    
class output_processor_class:
    def __init__(self):
        pass