import json
from sys import argv
from os.path import join
from pypdf import PdfReader, PdfWriter

input_folder, output_folder = argv[1:]

class inputProcessorClass:
    def __init__(self):
        self.inputPdf = PdfHandler(join(input_folder, "document.pdf"))
        self.option = "" # merge, split, or text
        self.inputString = ""
        self.inputWordList = []
        self.previousPagesOrSentences = 0
        self.futurePagesOrSentences = 0
        
    def processWords(self):
        inputWords = []
        currentWord = ""
        for char in self.inputString: # iterate through all characters in the input string
            currentWord += char
            end = currentWord[-1:]
            if not (end == "|"):
                continue
            inputWords.append(currentWord[:-1]) # if end char is the word separator, we will append it to our list of words
            currentWord = ""
        inputWords.append(currentWord) # the last word doesn't have a pipe (|) at the end, so we append that manually because it's outside of the condition
        self.inputWordList = inputWords
        
    def processInputs(self):
        inputPath = join(input_folder, "document.pdf")

        try:
            pdf_reader = PdfReader(inputPath)
            self.pages = pdf_reader._get_num_pages()

            with open(join(input_folder, "variables.dictionary")) as f:
                data = json.load(f)
                self.option = data["options"]
                self.inputString = data["text"]
                self.processWords() # sets inputWordList after processing
                self.previousPagesOrSentences = data["beforeTarget"]
                self.futurePagesOrSentences = data["afterTarget"]
        except Exception as e:
            print(f"An error occurred while processing inputs: {e}")

    def alterPageSelection(self, pageList):
        try:
            pagesBefore = self.getPreviousPages()
            pagesAfter = self.getFuturePages()
            newPageList = []
            for i, pageInOriginalDocument in enumerate(pageList):
                for count, pageToAdd in enumerate(range(pageInOriginalDocument, pagesBefore, -1), start=1):
                    if i == 0:  # handle first page separately
                        previousPage = pageList[i]
                    else:
                        previousPage = pageList[i - 1]
                    if pageToAdd <= previousPage:
                        break
                    if i - count <= 0:  # if the previous page we are adding is <= 0, break
                        break
                    newPageList.append(pageToAdd)  # Add page to the new list
                newPageList.append(pageInOriginalDocument)  # Add the original page to the new list
                for count, pageToAdd in enumerate(range(pageInOriginalDocument, pagesAfter), start=1):
                    if i == len(pageList) - 1:  # handle last page separately
                        nextPage = pageList[i]
                    else:
                        nextPage = pageList[i + 1]
                    if pageToAdd >= nextPage:
                        break
                    if i + count > self.pages:  # if the next page we are adding is > max pages in pdf, break
                        break
                    newPageList.append(pageToAdd)  # Add page to the new list
            return newPageList  # Return the new modified page list
        except Exception as e:
            print(f"An error occurred while altering page selection: {e}")


    def getPages(self):
        return self.pages
    
    def getPdf(self):
        return self.inputPdf
    
    def getOption(self):
        return self.option
    
    def getInputWordList(self):
        return self.inputWordList
    
    def getInputString(self):
        return self.inputWordString
    
    def getPreviousPagesOrSentences(self):
        return self.previousPagesOrSentences
    
    def getFuturePagesOrSentences(self):
        return self.futurePagesOrSentences

class outputProcessorClass:
    def __init__(self):
        self.outputPath = join(output_folder, "outputDocument.pdf")
        
    def getOutPath(self):
        return self.outputPath
        
class PdfHandler:
    def __init__(self, inputPath):
        self.path = inputPath
    
    def searchWords(self, inputWords):
        foundPages = []
        pdf_reader = PdfReader(self.path)
        for pageNum in range(pdf_reader._get_num_pages()):
            page = pdf_reader._get_page(pageNum)
            for word in inputWords: # iterate through each word in all input words
                if(word in page.extract_text()):
                    foundPages.append(pageNum)
                    break
        return foundPages
    
    def mergePages(self, pages):
        try:
            outputProcessor = outputProcessorClass()
            pdf_reader = PdfReader(self.path)
            pdf_writer = PdfWriter()
            for pageNum in pages:
                pdf_writer.add_page(pdf_reader.pages[pageNum])
            with open(outputProcessor.getOutPath(), "wb") as f:
                pdf_writer.write(f)
        except Exception as e:
            print(f"An error occurred while merging pages: {e}")

    def splitPages(self, pages):
        pass

try:
    inputProcessor = inputProcessorClass()
    inputProcessor.processInputs() # Initialize inputs, put words into inputWordList
    outputProcessor = outputProcessorClass()
    inputPdf = inputProcessor.getPdf()

    wordList = inputProcessor.getInputWordList()
    pagesWithSelectedWordList = inputPdf.searchWords(wordList) # Find all pages that have one or more words from inputWordList

    if not pagesWithSelectedWordList: # If there are no pages that have the words, exit.
        print("No pages found with the selected word(s).")
        exit()

    if(inputProcessor.getOption() == "merge"):
        pagesWithSelectedWordList = inputProcessor.alterPageSelection(pagesWithSelectedWordList) # alter the pageList with pagesBefore and pagesAfter
        inputPdf.mergePages(pagesWithSelectedWordList) # merge the pages and output it (built-in to the mergePages method)

    if(inputProcessor.getOption() == "split"):
        pagesWithSelectedWordList = inputProcessor.alterPageSelection(pagesWithSelectedWordList) # alter the pageList with pagesBefore and pagesAfter
        inputPdf.splitPages(pagesWithSelectedWordList)

    if(inputProcessor.getOption() == "text"):
        pass
except Exception as e:
    print(f"An error occurred: {e}")
