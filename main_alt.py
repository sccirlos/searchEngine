##################################################################################################
# Created By: Srikanth Akiti, Sonya Cirlos, Jose Ruben Espinoza, Marlon Martinez, Albert Trevino #
# Project Title: Web Search Project                                                              #
# Date Range: Summer I 2022                                                                      #
# Short Description: Web search engine implementation using an inverted index tables.            #
##################################################################################################

# Import necessary libraries
import os
import zipfile
from bs4 import BeautifulSoup
from math import log2

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



#def cosineSimRanking(query,relevantDocs):

def webSearch(doc):
    print("Now the search beings:")
    keysearch = input("enter a search key=>")
    while (keysearch != ""):
        keysearch = keysearch.split()
        #phrsalQuery(keysearch)
        for thing in keysearch:
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
