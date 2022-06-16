# Import necessary libraries
import os
import zipfile
from bs4 import BeautifulSoup
#import nltk
#nltk.download('punkt')

# Unzip Jan.zip if necessary.
def unzipContents():
    if 'Jan' not in os.listdir():
        with zipfile.ZipFile('cheDoc.zip', 'r') as zip_ref:
            zip_ref.extractall()
    else:
        print("Folder already there...")

# Traverse HTML files, returns a inverted index hash table.
def traverseHTML(htmlFiles):
    stop_words = ['a', 'an', 'the', 'of']
    invertedIndexDic = {}
    docTable = {}

    for item in htmlFiles:

        docTable[item] = {
            'doc vec length': 0,
            'max freq': 0,
            'url': str("./cheDoc/"+str(item))

        }

        with open(item) as file:
            soup = BeautifulSoup(file, "html.parser")
            entry = {}

            # Tokenize text
            currentFileText = soup.get_text().lower().split()

            # Strip text of numerical and stop words
            currentFileText = [word for word in currentFileText if word.isalpha() and word not in stop_words]
            # Tiny hack: convert current text to file
            for word in list(dict.fromkeys(currentFileText)):
                if word not in invertedIndexDic.keys():
                    invertedIndexDic[word] = {
                        'df': 1,
                        'link': []
                    }
                else:
                    invertedIndexDic[word]['df'] += 1

                    #invertedIndexDic[word]['link'].append(1)
    return invertedIndexDic, docTable

def webSearch(doc):
    print("Now the search beings:")
    keysearch = input("enter a search key=>")
    while (keysearch != ""):
        for key, value in doc.items():
            if " " + keysearch + " " in value:
                print("found a match: ./cheDoc/"+str(key))
        keysearch = input("enter a search key=>")
    print("Bye")

if __name__ == '__main__':
    unzipContents()

    # Obtain all files in Jan directory
    allHTMLFiles = os.listdir('cheDoc')

    # cd into new Jan directory.
    os.chdir("cheDoc")

    # Store HTML files into a Dic
    completeDocumentsDic = traverseHTML(allHTMLFiles)
    print(completeDocumentsDic[0])
    print(completeDocumentsDic[1])
    # Engine
    #webSearch(completeDocumentsDic)
