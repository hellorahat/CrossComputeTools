import json
import re
import math
import pandas as pd
from sys import argv
from os.path import join

input_folder, output_folder = argv[1:]

class input_processor_class:
    def __init__(self):
        self.input_path = join(input_folder, "input.csv")
        
        with open(join(input_folder, "variables.dictionary")) as f:
            data = json.load(f)
            self.suppression_columns = data["suppression_columns"]
            self.words_to_suppress = data["words_to_suppress"]
            self.numbers_to_round = data["numbers_to_round"]
            self.locations_to_generalize = data["locations_to_generalize"]
            
class output_processor_class:
    def __init__(self):
        self.output_path = join(output_folder, "out.csv")
    
class suppressor_class:
    def __init__(self, suppression_columns, words_to_suppress):
        # Initialize variables
        self.columns = {}
        self.words = {}
        
        # Process data
        self.process_string(suppression_columns, self.columns)
        self.process_string(words_to_suppress, self.words)

    def process_string(self, s, dictionary):
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
            if len(parts) == 2:  # If there are 2 parts, this means that the user specified how many characters should be suppressed
                col = parts[0]
                chars_to_suppress = parts[1]
            else: # otherwise, supress the entire entry
                col = entry
                chars_to_suppress = '0'  # '0' indicates to suppress the entire word
            
            # # Check to see if the amount of characters to suppress doesn't exceed the length of the word
            # if(abs(int(chars_to_suppress)) >= len(col)):
            #     chars_to_suppress = '0' # '0' indicates to suppress the entire word

            dictionary[col] = chars_to_suppress
        
    def suppress_data(self, df):
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
                    cell_value = str(df.iat[row_index,col_index])
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
                                            
        
class number_rounder:
    def __init__(self, digits_to_round):
        # Initialize variables
        self.columns = {}

        # Process data
        self.process_string(digits_to_round, self.columns)
    
    def process_string(self, s, dictionary):
        entries = s.split("\n")
        for entry in entries:
            parts = entry.split(":")
            if len(parts) == 2:
                col = parts[0]
                digits_to_round = parts[1]
            else: # if the digit to round to is not specified, round to leftmost digit
                col = entry
                digits_to_round = "-1" # -1 means to round the leftmost digit

            dictionary[col] = digits_to_round

    def round_df_cols(self, df):
        for col_name, digits_to_round in self.columns.items():
            if col_name in df.columns:
                for i, cell in enumerate(df[col_name]):
                    df.at[i,col_name] = self._round(cell,digits_to_round)

    def _round(self, s, digit):
        num = int(s)
        digit = int(digit)
        if num == 0:
            return 0

        num_abs = abs(num)
        sign = -1 if num < 0 else 1

        # Calculate the power of 10 for the given digit position
        power = int(math.log10(num_abs))
        if digit < 0:
            power = power + digit + 1
        else:
            power = power - digit + 1

        # Calculate the rounding base
        base = num_abs / (10**power)

        # Perform rounding
        if base >= 5:
            base = math.ceil(base)
        else:
            base = math.floor(base)

        # Calculate the rounded number
        rounded_num = base * (10**power)

        return rounded_num * sign

class location_generalizer:
    def __init__(self):
        pass

    def process_string(self):
        pass

if __name__ == "__main__":
    input_processor = input_processor_class()
    output_processor = output_processor_class()
    df = pd.read_csv(input_processor.input_path)
    df.astype(str)
    
    suppressor = suppressor_class(input_processor.suppression_columns, input_processor.words_to_suppress)
    suppressor.suppress_data(df)

    rounder = number_rounder(input_processor.numbers_to_round)
    rounder.round_df_cols(df)

    df.to_csv(output_processor.output_path, index=False)