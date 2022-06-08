# I don't know, description here?
import os
import zipfile
from bs4 import BeautifulSoup

# Unzip Jan.zip if necessary.
def unzipContents():
    if 'Jan' not in os.listdir():
        with zipfile.ZipFile('Jan.zip', 'r') as zip_ref:
            zip_ref.extractall()
    else:
        print("Folder already there...")

# Traverse HTML files, returns a dictionary of {fileName: fileText}
# the values have escape characters, want to avoid this, maybe use NLTK?
def traverseHTML(htmlFiles):
    documents = {}
    for item in htmlFiles:
        with open(item) as file:
            soup = BeautifulSoup(file, "html.parser")
            currentFileText = soup.get_text().lower()
            textCleaned = currentFileText.replace("^[A-Za-z]*$", "") # only keep alpha, I don't like this
            documents.update({str(item) : str(textCleaned)})
    return documents

def webSearch(doc):
    print("Now the search beings:")
    keysearch = input("enter a search key=>")
    while (keysearch != ""):
        for key, value in doc.items():
            if " " + keysearch + " " in value:
                print("found a match: ./Jan/"+str(key))
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

    # Engine
    webSearch(completeDocumentsDic)