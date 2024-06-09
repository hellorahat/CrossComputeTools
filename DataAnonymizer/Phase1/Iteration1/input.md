# DataAnonymizer
#### This tool uses techniques such as suppression and generalization to anonymize large sets of data to protect privacy.

## Step 1: Upload the CSV
#### Upload your dataset in this step.
{ csv }

## Step 2: Specify Columns to Suppress
#### Input the names of the columns here. Each column should be in a separate line. Specify characters to suppress by adding a colon followed by an integer.
For example - ColumnName:3
- 0 (or no integer) indicates that all characters will be suppressed
- An integer n indicates to suppress the first n characters
- A negative integer n indicates to suppress the last n characters

{ suppression_columns }

## Step 3: Specify Words to Suppress
#### Separate words in a separate line
{ words_to_suppress }

## Step 4: Specify Columns to Generalize
#### Input the names of the columns here. Each column should be in a separate line. Specify the digit to round to by adding a colon followed by an integer.
#### Location columns can also be generalized.
{ generalization_columns }