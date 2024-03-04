import json
from sys import argv
from os.path import join
from pypdf import PdfReader, PdfWriter
input_folder, output_folder = argv[1:]

class inputClass:
    def __init__(self):
        self.pdf = document
        self.option = "" # merge, split, or text
        self.inputString = ""
        self.inputWordList = []
        self.previousPages = 0
        self.futurePages = 0
        self.getInputs()
    def getInputs(self):
        self.pdf = document(join(input_folder, "document.pdf"))
        with open(join(input_folder, "variables.dictionary")) as f:
            d = json.load(f)
            self.option = d["options"]
            self.inputString = d["text"]
            self.processWords() # sets inputWordList after processing
            self.previousPages = d["beforeTarget"]
            self.futurePages = d["afterTarget"]
    def processWords(self):
        inputWords = []
        currentWord = ""
        for char in self.inputString:
            currentWord += char
            if(len(currentWord) <= 1):
                continue
            end = currentWord[-1:]
            if not (end == "|"):
                continue
            inputWords.append(currentWord[:-1])
            currentWord = ""
        inputWords.append(currentWord)
        self.inputWordList = inputWords
    def getPdf(self):
        return self.pdf
    def getOption(self):
        return self.option
    def getInputWordList(self):
        return self.inputWordList
    def getPreviousPages(self):
        return self.previousPages
    def getFuturePages(self):
        return self.futurePages
        
class document:
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
    def mergePages(self, allPages, outPath):
        pdf_reader = PdfReader(self.path)
        pdf_writer = PdfWriter()
        for pageNum in allPages:
            pdf_writer.add_page(pdf_reader.pages[pageNum])
        with open(outPath, "wb") as f:
            pdf_writer.write(f)
        
class documentList:
    def __init__(self):
        self.documents = []
    # def __str__():
    #     pass

inputs = inputClass()
pdf = document(join(input_folder, "document.pdf"))
with open(join(input_folder, "variables.dictionary")) as f:
    d = json.load(f)
    inputWordString = d["text"]
pageList = pdf.searchWords(inputs.getInputWordList())
if not pageList:
    print("list empty")
    exit()
if(inputs.getOption() == "merge"):
    outPath = join(output_folder, "outputDocument.pdf")
    mergedPdf = pdf.mergePages(pageList, outPath)
