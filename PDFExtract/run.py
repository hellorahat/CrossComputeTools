import json
from sys import argv
from os.path import join
import os
from pypdf import PdfReader, PdfWriter
from zipfile import ZipFile
from pdfminer.high_level import extract_text
import re

input_folder, output_folder = argv[1:]

class inputProcessorClass:
    def __init__(self):
        self.inputPdf = PdfHandlerClass(join(input_folder, "document.pdf"))
        self.inputPath = join(input_folder, "document.pdf")
        self.option = "" # merge, split, or text
        self.inputString = ""
        self.inputWordList = []
        self.previousPages = -1
        self.futurePages = -1
        self.previousSentences = -1
        self.futureSentences = -1
        self.pageCount = 0
        
    def processWords(self):
        inputWords = []
        currentWord = ""
        for char in self.inputString: # iterate through all characters in the input string
            currentWord += char
            end = currentWord[-1:]
            if not (end == "\n"):
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
            self.pageCount = pdf_reader._get_num_pages()
            with open(join(input_folder, "variables.dictionary")) as f:
                data = json.load(f)
                self.option = data["options"]
                self.inputString = data["textToExtract"]
                self.processWords() # sets inputWordList after processing
                
                # set pages/sentences before and after
                if self.option == "text":
                    self.previousSentences = data["beforeTarget"]
                    self.futureSentences = data["afterTarget"]
                else:
                    self.previousPages = data["beforeTarget"]
                    self.futurePages = data["afterTarget"]
        except Exception as e:
            print(f"An error occurred while processing inputs: {e}")

    def alterMergedPageSelection(self, pageList): 
        """
        Generate a 1D list of page numbers including pages before and after according to the selection.

        Parameters:
            page_list (list): List of selected page numbers.

        Returns:
            list: Modified page list.
        """
        try:
            pageCount = self.getPageCount()
            pagesBefore = self.getPreviousPages()
            pagesAfter = self.getFuturePages()
            newPageList = []
            
            for originalPage in pageList:
                # append all pages before original
                for v in range(originalPage-pagesBefore,originalPage):
                    
                    if v < 0: # page can't be negative
                        break
                    if v in newPageList: # page can't already be in the altered list
                        break
                    newPageList.append(v)
                
                # append original page and all pages after
                for v in range(originalPage, originalPage+(pagesAfter+1)):
                    
                    if v > pageCount: # page can't be greater than total pages in pdf
                        break
                    if v in newPageList: # page can't already be in the altered list
                        break
                    newPageList.append(v)
                    
            return newPageList  # Return the new modified page list
        except Exception as e:
            print(f"An error occurred while altering page selection: {e}")
            
    def alterSplitPageSelection(self, pageList):
        """
        Generate a 2D list of page ranges including pages before and after according to the selection.

        Parameters:
            page_list (list): List of selected page numbers.

        Returns:
            list[list]: Modified page list.
        """
        try:
            pageCount = self.getPageCount()
            pagesBefore = self.getPreviousPages()
            pagesAfter = self.getFuturePages()
            newPageList = []
            
            for originalPage in pageList:
                pageRange = []
                # append all pages before original
                for v in range(originalPage-pagesBefore,originalPage):
                    
                    if v < 0: # page can't be negative
                        break
                    if v in newPageList: # page can't already be in the altered list
                        break
                    pageRange.append(v)
                
                # append original page and all pages after
                for v in range(originalPage, originalPage+(pagesAfter+1)):
                    
                    if v > pageCount: # page can't be greater than total pages in pdf
                        break
                    if v in newPageList: # page can't already be in the altered list
                        break
                    pageRange.append(v)
                    
                newPageList.append(pageRange) # append the range to the updated list
            return newPageList  # Return the new modified page list
        except Exception as e:
            print(f"An error occurred while altering page selection: {e}")

    def getPath(self):
        return self.inputPath
    
    def getPages(self):
        return self.pages
    
    def getPdf(self):
        return self.inputPdf
    
    def getOption(self):
        return self.option
    
    def getPageCount(self):
        return self.pageCount
    
    def getInputWordList(self):
        return self.inputWordList
    
    def getInputString(self):
        return self.inputWordString
    
    def getPreviousPages(self):
        return self.previousPages
    
    def getFuturePages(self):
        return self.futurePages
    
    def getPreviousSentences(self):
        return self.previousSentences
    
    def getFutureSentences(self):
        return self.futureSentences

class outputProcessorClass:
    def __init__(self):
        self.mergeOutputPath = join(output_folder, "outputDocument.pdf")
        self.splitOutputPath = join(output_folder, "outputZip.zip")
        self.textOutputPath = join(output_folder, "outputText.txt")
        
    def getMergedOutPath(self):
        return self.mergeOutputPath
    
    def getSplitOutPath(self):
        return self.splitOutputPath
    
    def getTextOutPath(self):
        return self.textOutputPath
        
class PdfHandlerClass:
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
            with open(outputProcessor.getMergedOutPath(), "wb") as f:
                pdf_writer.write(f)
        except Exception as e:
            print(f"An error occurred while merging pages: {e}")

    def splitPages(self, rangeList):
        try:
            outputProcessor = outputProcessorClass()
            pdf_reader = PdfReader(self.path)
            with ZipFile(outputProcessor.getSplitOutPath(), "w") as zip:
                for i, range in enumerate(rangeList):
                    pdf_writer = PdfWriter()
                    
                    for page in range:
                        pdf_writer.add_page(pdf_reader.pages[page])
                        
                    with open(f"pdf_{i}.pdf", "wb") as f:
                        pdf_writer.write(f)
                        
                    zip.write(f.name, os.path.basename(f.name))
                    os.remove(f.name)
        except Exception as e:
            print(f"An error occurred while splitting pages: {e}")

class textHandlerClass:
    def sentenceTokenizer(self, text):
        sentence_endings = r'[.!?]'
        sentences = re.split(sentence_endings, text)
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()] # remove white space
        return sentences
    
    def pdfToText(self, pdfPath):
        return extract_text(pdfPath)
            
    def getSentences(self, pdfPath, wordList):
        try:
            sentencesBefore = inputProcessor.getPreviousSentences()
            sentencesAfter = inputProcessor.getFutureSentences()
            outputText = ""
            
            text = self.pdfToText(pdfPath)
            sentenceList = self.sentenceTokenizer(text)
            
            for i,sentence in enumerate(sentenceList):
                if any(phrase in sentence for phrase in wordList): # if word is in sentence
                    # get previous sentences (exclusive)
                    for j in range(max(0, i - sentencesBefore), i):
                        outputText = sentenceList[j] + outputText + " "
                    
                    # get future sentences (inclusive)
                    for j in range(i, min(len(sentenceList), i + sentencesAfter + 1)):
                        outputText = outputText + sentenceList[j] + " "
                    outputText += "\n"
                
            return outputText
        except Exception as e:
            print(f"An error occured in getSentences(): {e}")
                        
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
        pagesWithSelectedWordList = inputProcessor.alterMergedPageSelection(pagesWithSelectedWordList) # alter the pageList with pagesBefore and pagesAfter
        inputPdf.mergePages(pagesWithSelectedWordList) # merge the pages and output it (built-in to the mergePages method)

    if(inputProcessor.getOption() == "split"):
        pagesWithSelectedWordList = inputProcessor.alterSplitPageSelection(pagesWithSelectedWordList) # alter the pageList with pagesBefore and pagesAfter
        inputPdf.splitPages(pagesWithSelectedWordList)

    if(inputProcessor.getOption() == "text"):
        textHandler = textHandlerClass()
        text = textHandler.getSentences(inputProcessor.getPath(), inputProcessor.getInputWordList())
        with open(outputProcessor.getTextOutPath(), "w") as text_file:
            text_file.write(text)
except Exception as e:
    print(f"An error occurred in Main: {e}")
