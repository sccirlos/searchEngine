##################################################################################################
# Created By: Srikanth Akiti, Sonya Cirlos, Jose Ruben Espinoza, Marlon Martinez, Albert Trevino #
# Project Title: Web Search Project                                                              #
# Date Range: Summer I 2022                                                                      #
# Short Description: Web search engine implementation using an inverted index tables.            #
##################################################################################################

# Import necessary libraries
from zipfile import ZipFile
from bs4 import BeautifulSoup
from math import log2, sqrt
from queryProcessing import searchFunctions

# Store zip file in archive
archive = ZipFile('rhf.zip', 'r')
# Top 100 most frequently used words (excluding or, and, but). source wiki
stop_words = ['the', 'be', 'to', 'of', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he',
              'as', 'you', 'do', 'at', 'this', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
              'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about',
              'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know',
              'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than',
              'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two',
              'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give',
              'day', 'most', 'us']


docTable = {}
invertedIndexDic = {}
def breadthSearch(file='rhf/index.html'):

    soup = BeautifulSoup(archive.read(file).decode('utf8'), "html.parser")
    if file in docTable:
        return
    docTable[file] = {
        'doc vec length': 0,
        'max freq': 0,
        'url': str(file)
    }

    currentFileText = soup.get_text().lower().split()

    currentFileText = [word for word in currentFileText if word.isalpha() and word not in stop_words]

    for word in list(dict.fromkeys(currentFileText)):
        # Here we build up our inverted index table.
        if word not in invertedIndexDic.keys():
            invertedIndexDic[word] = {
                'df': 1,
                'link': [[file, currentFileText.count(word),
                          [index for index, item in enumerate(currentFileText) if item == word],
                          0]]
            }
        else:
            invertedIndexDic[word]['df'] += 1
            if file not in invertedIndexDic[word]['link']:
                invertedIndexDic[word]['link'].append([file, currentFileText.count(word),
                                                       [index for index, item in enumerate(currentFileText)
                                                        if item == word],
                                                       0])
    for entry in [value['link'] for key, value in invertedIndexDic.items()]:
        for subEntry in entry:
            if docTable[file]['max freq'] < subEntry[1] and subEntry[0] == file:
                docTable[file]['max freq'] = subEntry[1]

    allLinks = [links.get('href') for links in soup.find_all('a', href=True)]
    for link in allLinks:
        if link not in docTable and ".." not in link and ":" not in link and "#" not in link and "/" not in link[-1]:
            path = '/'.join(file.split("/")[:-1]) + "/"
            try:
                breadthSearch(path+link)
            except:
                pass

def updateIndexTFIDF():
    for key, value in invertedIndexDic.items():
        df = invertedIndexDic[key]['df']
        for entry in value['link']:
            docOfIntrest = entry[0]
            maxfreq = docTable[docOfIntrest]['max freq']
            freq = entry[1]
            idf = log2(len(docTable) / (df + 1)) + 1
            tf_idf = (freq / maxfreq) * idf
            entry[3] = tf_idf

def updateDocTableVectorLenth():
    for doc in docTable:
        for key, value in invertedIndexDic.items():
            for linkData in value['link']:
                if linkData[0] == doc:
                    docTable[doc]['doc vec length'] += (linkData[3] * linkData[3])
if __name__ == '__main__':
    # Reading zip file, code segment from Dr. Chen.
    # allHTMLFiles = [name for name in archive.namelist() \
    #                  if name.endswith('.html') or name.endswith('.htm')]
    print("starting traversal")
    breadthSearch()
    print("done with traversal")
    # Update inverted index table to have tf-idf values
    updateIndexTFIDF()
    print("done updating index")
    # Update doc vector lengths within docTable
    print("updating vector lengths now...")
    updateDocTableVectorLenth

    # Store HTML files into a Dic
    #invertedIndex, documentInformation = traverseHTML(allHTMLFiles)
    #print(invertedIndexDic)
    searchFunctions.webSearch(invertedIndexDic, docTable)
