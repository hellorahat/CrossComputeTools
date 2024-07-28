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

## Step 4: Specify Numbers to Round
#### Input columns where numbers should be rounded. Specify digit to round to by adding a colon followed by an integer.
For example - Salary:3 - will round the Salary column to the 3rd digit.

{ numbers_to_round }

## Step 5: Specify Locations to Generalize
#### Input the names of the columns here. Each column should be in a separate line. Specify what region to generalize to by adding a colon followed by region.
For example:
- LocationColumn:city
- LocationColumn:state
- LocationColumn:country

{ locations_to_generalize }
