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
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets


# Import necessary libraries
import os
import zipfile
from bs4 import BeautifulSoup
from math import log2


# adding mainwindow
class MainWindow(QMainWindow):
    def __init__(self):
       super(MainWindow, self).__init__()
       self.setupUi(self)



 # Unzip Jan.zip if necessary. "Folder already there..." prints if the extracted folder is already present.
def unzipContents():
    if 'Jan' not in os.listdir():
        with zipfile.ZipFile('Jan.zip', 'r') as zip_ref:
            zip_ref.extractall()
    else:
        print("Folder already there...")

# Traverse HTML files, returns a inverted index hash table.
def traverseHTML(htmlFiles):

    stop_words = ['a', 'an', 'the', 'of'] # removal of stop words
    numOfDocuments = len(htmlFiles)

    invertedIndexDic = {}
    docTable = {}

    # Begin creating inverted index and document list (stored in docTable) hash maps.
    for item in htmlFiles:

        # Initialize the creation of the document list.
        docTable[item] = {
            'doc vec length': 0,
            'max freq': 0,
            'url': str("./Jan/"+str(item))

        }

        with open(item) as file:
            soup = BeautifulSoup(file, "html.parser")

            # Tokenize text
            currentFileText = soup.get_text().lower().split()

            # Strip text of numerical and stop words
            currentFileText = [word for word in currentFileText if word.isalpha() and word not in stop_words]

            # Tiny hack: convert current text to file
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
            # Update max freq in docTable
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
            docTable[docOfIntrest]['doc vec length'] += (tf_idf * tf_idf)
            #print(tf_idf)

    return invertedIndexDic, docTable

#this function will search for phrases based on the users input
def phraseSearch(doc):
    listwords=[]

    print("Now the search beings:")
    keysearch = input("enter a search key, quit by hitting enter twice=>")
    while (keysearch != ""):
        keysearch = keysearch.split()
        for word in keysearch:
            #print(doc[0][word]['link'])
            listwords.append(doc[0][word]['link'])
        listwords = tuple(listwords)
        print("type of listwords: ", type(listwords))
        print("list of all words in list: ", listwords)

        intersectionlist=()
        #this will iterate though out the whole list to compare the documents and only get the ones that
        #are needed in order to get the best ranked documents for the phrasal search
        for link in listwords:
            print("THIS IS I: ", link)
            for data in link:
                print("this is J: ", data[0])
                if(listwords[link][data] == listwords[link+1][data+1]):
                    intersectionlist = data[0]

        print("SHOULD BE ONLY INTERSECTION DOCTUMETNS", intersectionlist)
        #compare the documents based on the ones that are the same

        #print(type(cleanlist))

       # for item in range(len(listwords) - 1):
        #    temp= set(listwords[item] & set(listwords[item+1]))
         #   interlist = interlist & temp
        #print(interlist)

        #1st is the 1st word[0]
        #2nd [0] is the list of documents of the word
        #3rd [0] is only the documments of that word??

        #print("dog: ", listwords[0][0])
        #print("cat: ", listwords[1])

        # for key, value in doc.items():
        #    if " " + keysearch + " " in value:
        #        print("found a match: ./cheDoc/"+str(key))

        keysearch = input("enter a search key=>")
    print("Bye")



#def cosineSimRanking(query,relevantDocs):

def webSearch(doc):
    print("Now the search beings:")
    keysearch = input("enter a search key=>")
    while (keysearch != ""):
        keysearch = keysearch.split()
        phraseSearch(keysearch)
        
        #Traverses through the list if the word matches and,or, or but it'll
       # conduct the boolean search. Currently only works with 2 terms'''
        for thing in keysearch:
    
            if 'and' in keysearch:
                index = keysearch.index('and')
                term1 = keysearch[index-1]
                term2 = keysearch[index+1]
                if term1 and term2 in doc[0]:
                    print(doc[0][term1]['link'])
                    print(doc[0][term2]['link'])

                    break;
                            

            elif 'or' in keysearch:
                index = keysearch.index('or')
                term1 = keysearch[index-1]
                term2 = keysearch[index+1]
                if term1 or term2 in doc[0]:
                    print(doc[0][term1]['link'])
                else:
                    print(doc[0][term2]['link'])
                    break;
                            

            elif 'but' in keysearch:
                index = keysearch.index('but')
                term1 = keysearch[index-1]
                term2 = keysearch[index+1]
                print(doc[0][term1]['link'])
                break;
                            

            else:
                print(doc[0][thing]['link'])
        keysearch = input("enter a search key=>")
    print("Bye")

if __name__ == '__main__':
    unzipContents()

    # Obtain all files in Jan directory
    allHTMLFiles = os.listdir('Jan')

    # cd into new Jan directory.
    os.chdir("Jan")

    # Store HTML files into a Dic
    completeDocumentsDic = traverseHTML(allHTMLFiles)

    webSearch(completeDocumentsDic)
    
    #print(completeDocumentsDic[1])
    #print(completeDocumentsDic[1])
    #print(completeDocumentsDic[0]['cat'])
  


    #if __name__ == "__main__":
    # App Stuff
   # app = QApplication(sys.argv)
    #w = Ui_MainWindow()
    #w.show()
   # sys.exit(app.exec_())
    #
