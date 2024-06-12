import json
import re
import pandas as pd
from sys import argv
from os.path import join

input_folder, output_folder = argv[1:]

def process_string(s, dictionary):
    """
    This function processes string s data into a dictionary.
    It will be stored as string:chars_to_suppress
    
    Parameters:
    s: The string to be processed.
    dictionary: The dictionary to process the data into. 
    """    
    entries = s.split("\n")
    for entry in entries:
        parts = entry.split(":")
        if len(parts) == 2:  # This indicates that the user specified how many characters should be suppressed
            col = parts[0]
            chars_to_suppress = parts[1]
        else:
            col = entry
            chars_to_suppress = '0'  # '0' indicates to suppress the entire word
        
        # Check to see if the amount of characters to suppress doesn't exceed the length of the word
        if(abs(int(chars_to_suppress)) >= len(col)):
            chars_to_suppress = '0' # '0' indicates to suppress the entire word

        dictionary[col] = chars_to_suppress


class input_processor_class:
    def __init__(self):
        self.input_path = join(input_folder, "input.csv")
        
        with open(join(input_folder, "variables.dictionary")) as f:
            data = json.load(f)
            self.generalization_columns = data["generalization_columns"]
            self.suppression_columns = data["suppression_columns"]
            self.words_to_suppress = data["words_to_suppress"]
                
class output_processor_class:
    def __init__(self):
        self.output_path = join(output_folder, "out.csv")
    
class suppressor_class:
    def __init__(self, suppression_columns, words_to_suppress):
        # Initialize variables
        self.columns = {}
        self.words = {}
        
        # Process data
        process_string(suppression_columns, self.columns)
        process_string(words_to_suppress, self.words)
        
    def suppress_data(self, csv_path):
        df = pd.read_csv(csv_path)
        df = df.astype(str)
        # Suppress data for columns
        for col_name, chars_to_suppress in self.columns.items():
            if col_name in df.columns:
                for i, cell in enumerate(df[col_name]):
                    df.at[i,col_name] = self.suppress(cell,chars_to_suppress)
                        
        # Iterate through every cell in the dataframe to locate each word
        for row_index in range(df.shape[0]):
            for col_index in range(df.shape[1]):
                # Suppress if word is found
                for word_to_suppress, chars_to_suppress in self.words.items():
                    cell_value = df.iat[row_index,col_index]
                    cell_words = re.split(f"({word_to_suppress})", cell_value)
                    for i, cell_word in enumerate(cell_words):
                        if word_to_suppress == cell_word:
                            cell_words[i] = self.suppress(word_to_suppress, chars_to_suppress)
                            df.iat[row_index, col_index] = ''.join(cell_words)
                
        return df
    
    def suppress(self, s, num):
        if(int(num) == 0):
            return self._suppress_all(str(s))
        elif(int(num) > 0):
            return self._suppress_first_chars(str(s), int(num))
        elif(int(num) < 0):
            return self._suppress_last_chars(str(s), abs(int(num)))
                        
    def _suppress_all(self, s):
        result = '*' * len(s)
        return result
    
    def _suppress_first_chars(self, s, num):
        return '*' * num + s[num:]
    
    def _suppress_last_chars(self, s, num):
        return s[:-num] + '*' * num
                                            
        
class generalizer_class:
    def __init__(self, generalization_columns):
        # Initialize variables
        self.columns = {}
        
        # Process Data
        process_string(generalization_columns, self.columns)


### Main ###

input_processor = input_processor_class()
output_processor = output_processor_class()

suppressor = suppressor_class(input_processor.suppression_columns, input_processor.words_to_suppress)
df = suppressor.suppress_data(input_processor.input_path)

generalizer = generalizer_class(input_processor.generalization_columns)

df.to_csv(output_processor.output_path, index=False)