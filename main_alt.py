##################################################################################################
# Created By: Srikanth Akiti, Sonya Cirlos, Jose Ruben Espinoza, Marlon Martinez, Albert Trevino #
# Project Title: Web Search Project                                                              #
# Date Range: Summer I 2022                                                                      #
# Short Description: Web search engine implementation using an inverted index tables.            #
##################################################################################################
# import libraries for interface
import sys
import mainwindow
import searchresultsUI
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QStackedWidget, QLineEdit
from PyQt5 import QtCore, QtGui, QtWidgets


# Import necessary libraries
import os
from zipfile import ZipFile
from bs4 import BeautifulSoup
from math import log2, sqrt



# adding mainwindow screen
class Ui_MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
      super().__init__()
      self.setupUi(self)
     
      self.pushButton.clicked.connect(self.gotoSearchPage)
      self.pushButton.clicked.connect(self.getQueryandSearch) # when search button is clicked it will connect to gotosearch()


    def gotoSearchPage(self):
        results = Ui_resultsUI()
        widget.addWidget(results)
        widget.setCurrentIndex(widget.currentIndex()+1) #stack of screens

    def getQueryandSearch(self, doc):
          # get query input
        query = self.lineEdit.text()
        

# displays results like completedocumentdictionary  
# results screen needs a go back to search button or something
class Ui_resultsUI(QDialog, searchresultsUI.Ui_resultsUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.pushButton.clicked.connect(self.getuserQuery)
        
   

# Store zip file in archive
archive = ZipFile('cheDoc.zip', 'r')


# Traverse HTML files, returns a inverted index hash table.
def traverseHTML(htmlFiles):
    
    # Traverse html files returning inverted index table and a document table
    # :param htmlFiles: Given zip file containing html files.
    # :return: inverted index table and document table
    
    # Removal of stop words to be used later.
    stop_words = ['a', 'an', 'the', 'of']

    numOfDocuments = len(htmlFiles)

    invertedIndexDic = {}
    docTable = {}

    # Begin creating inverted index and document list (stored in docTable) hash maps.
    for item in htmlFiles:

        # Initialize the creation of the document list.
        docTable[item] = {
            'doc vec length': 0,
            'max freq': 0,
            'url': str("./cheDoc/"+str(item))
        }

        with open(item) as file:
            soup = BeautifulSoup(file, "html.parser")

            # Tokenize and lower all text
            currentFileText = soup.get_text().lower().split()

            # Uses list comprehension to strip text of numerical and stop words.
            currentFileText = [word for word in currentFileText if word.isalpha() and word not in stop_words]

            # Tiny hack: Get unique words from currentFileText then build index table
            for word in list(dict.fromkeys(currentFileText)):

                # Here we build up our inverted index table.
                if word not in invertedIndexDic.keys():
                    invertedIndexDic[word] = {
                        'df': 1,
                        'link': [[item, currentFileText.count(word),
                                  [index for index, item in enumerate(currentFileText) if item == word],
                                  0]]
                    }
                else:
                    invertedIndexDic[word]['df'] += 1
                    if item not in invertedIndexDic[word]['link']:
                        invertedIndexDic[word]['link'].append([item, currentFileText.count(word),
                                                               [index for index, item in enumerate(currentFileText)
                                                                if item == word],
                                                               0])
            # Update 'max freq' in docTable
            for entry in [value['link'] for key, value in invertedIndexDic.items()]:
                for subEntry in entry:
                    if docTable[item]['max freq'] < subEntry[1] and subEntry[0] == item:
                        docTable[item]['max freq'] = subEntry[1]

    # Update inverted index table to have tf-idf values
    for key, value in invertedIndexDic.items():
        df = invertedIndexDic[key]['df']
        for entry in value['link']:
            docOfIntrest = entry[0]
            maxfreq = docTable[docOfIntrest]['max freq']
            freq = entry[1]
            idf = log2(numOfDocuments/(df + 1)) + 1
            tf_idf = (freq/maxfreq) * idf
            entry[3] = tf_idf

    # Update doc vector lengths within docTable
    for doc in htmlFiles:
        for key, value in invertedIndexDic.items():
            for linkData in value['link']:
                if linkData[0] == doc:
                    docTable[doc]['doc vec length'] += (linkData[3] * linkData[3])
    return invertedIndexDic, docTable



def rankBySecondElem(list):
    # Helper function to be used in cosineSimRanking.
    # :param list: list of the form [[docid1, rankingScore1], [docod2, rankingScore2]...
    # :return: Sorted list by second entry.
    return list[1]


def cosineSimRanking(intrestedPhrase, relevantDocs):
    # Ranks preform cosine similarity ranking.
    # :param intrestedPhrase: User query must be preprocessed as a list of words
    # :param relevantDocs: Hash table of document information
    # :return: Sorted rank list with entries [docid, cosine similarity score].
    rankedList = []
    for key, value in relevantDocs[1].items():
        normalization = 1 / sqrt(value['doc vec length'])
        summationList = []
        for word in intrestedPhrase:
            summationList.append([num[3] for num in relevantDocs[0][word]['link'] if num[0] == key])
        # flatten summationList, then sum numbers
        vecSum = sum([num for numArr in summationList for num in numArr])
        rankingScore = normalization * (1 / sqrt(len(intrestedPhrase)) * vecSum)
        rankedList.append([key, rankingScore])
    return sorted(rankedList, key=rankBySecondElem, reverse=True)



#this function will search for phrases based on the users input
def phrasalSearch(query, invertedIndex, docTable):
    
    # Preform phrasalSearch.
    # :param query: Search query.
    # :param invertedIndex: Inverted index
    # :param docTable: Document table.
    # :return: List of lists, by correlationg rank.
    
    query = query[1:len(query) - 1].lower().strip().split()
    if checkIndex(query,invertedIndex):
        print("Continue")
        if len(query) == 1:
            print(' '.join(query))
            booleanSearch(' '.join(query), invertedIndex, docTable)
            return
    else:
        "Last entry not valid."
    return 0



def booleanSearch(query, invertedIndex, docTable):
    query = query.split()
    if "and" in query:
        relevantDocsTemp = []
        toBeCleaned = []
        print("Conducting AND query...")
        # Get intersecting document set first
        for word in query:
            if word != "and":
                relevantDocsTemp.append([entry[0] for entry in invertedIndex[word]['link']])
                toBeCleaned.append([[entry[0], entry[3]] for entry in invertedIndex[word]['link']])
        intersectingDocs = set(relevantDocsTemp[0])
        for doc in relevantDocsTemp:
            intersectingDocs = intersectingDocs & set(doc)
        intersectingDocs = list(intersectingDocs)

        finalOutWithRanking = {}
        for entry in sum(toBeCleaned,[]):
            if entry[0] not in finalOutWithRanking:
                if entry[0] in intersectingDocs:
                    finalOutWithRanking[entry[0]] = entry[1]
            else:
                finalOutWithRanking[entry[0]] += entry[1]
        return list(map(list, sorted(list(finalOutWithRanking.items()),key=rankBySecondElem,reverse=True)))
    else:
        print("Conducting OR query...")
        relevantDocsTemp = []
        for word in query:
            if word != "or":
                relevantDocsTemp.append([[entry[0], entry[3]] for entry in invertedIndex[word]['link']])
        relevantDocsTemp = sum(relevantDocsTemp,[]) # flatten a 2d array
        relevantDocs = {}  # using dictionary for ease of merging and updating correlations
        for entry in relevantDocsTemp:
            if entry[0] not in relevantDocs:
                relevantDocs[entry[0]] = entry[1]
            else:
                relevantDocs[entry[0]] += entry[1]
        # Note, dictionary was converted into a list of tuples, the finally a list of lists. This is done
        # in order to ensure consistency with the output in phrasal search.
        return list(map(list, sorted(list(relevantDocs.items()),key=rankBySecondElem,reverse=True)))



def checkIndex(query, invertedIndex):
    
    # Implementing early stop. Check if query words are in inverted index or not.
    # :param query:
    # :param invertedIndex:
    # :return: True if words can be found, false otherwise.
    
    for word in query:
        if word != "and" or word != "or":
            if word not in invertedIndex:
                print(word + " not a valid entry")
                return False
    return True



def webSearch(invertedIndex, docTable):
    
    # Web engine console.
    # :param invertedIndex: Inverted index table.
    # :param docTable: Table containing doc information
    # :return:
    
    print("Now the search beings:")
    searchEntry = input("enter a search key=>")
    while (searchEntry != ""):
        # Check for phrasal first.
        if "\"" in searchEntry:
            print("Preforming phrasal search...")
            print(phrasalSearch(searchEntry, invertedIndex, docTable))
        elif len(searchEntry.split()) == 1:
            print("Only searching for one word...")
            print(booleanSearch(searchEntry, invertedIndex, docTable))
        else:
            print("Preforming boolean search...")
            print(booleanSearch(searchEntry, invertedIndex, docTable))
        searchEntry = input("enter a search key=>")
    print("Bye")




if __name__ == '__main__':
    # Reading zip file, code segment from Dr. Chen.
    allHTMLFiles = [name for name in archive.namelist() \
             if name.endswith('.html') or name.endswith('.htm')]

    # Store HTML files into a Dic
    invertedIndex, documentInformation = traverseHTML(allHTMLFiles)

    webSearch(invertedIndex, documentInformation)
    
    # App execution
    app = QApplication(sys.argv)
    mainui = Ui_MainWindow()
    widget = QStackedWidget()
    widget.addWidget(mainui)
    widget.setFixedHeight(600)
    widget.setFixedWidth(800)
    widget.show()
    sys.exit(app.exec_())
    
