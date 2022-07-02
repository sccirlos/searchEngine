import zipfile
from bs4 import BeautifulSoup
import json

archive = zipfile.ZipFile('rhf.zip', 'r')
hyperLinksPerHTML = {}

def breadthSearch(file='rhf/index.html', multiThread=True, layer = 0):
    soup = BeautifulSoup(archive.read(file).decode('utf8'), "html.parser")
    if file in hyperLinksPerHTML:
        return
    print(soup.find('title'))
    title = soup.find('title')
    title = title
    hyperLinksPerHTML[file] = title
    allLinks = [links.get('href') for links in soup.find_all('a', href=True) \
                if ".." not in links.get('href') and ":" not in links.get('href') and "#" not in links.get('href') \
                and "/" not in links.get('href')[-1]]

    for link in allLinks:
        if link not in hyperLinksPerHTML:
            path = '/'.join(file.split("/")[:-1]) + "/"
            try:
                if layer == 0:
                    layer += 1
                    breadthSearch(path + link, True, 1)
                else:
                    breadthSearch(path + link, False, 1)
            except:
                pass

def linksThreading(file,allLinks):
    for link in allLinks:
        if link not in hyperLinksPerHTML:
            path = '/'.join(file.split("/")[:-1]) + "/"
            try:
                breadthSearch(path + link, False, 1)
            except:
                pass
breadthSearch()
#print(hyperLinksPerHTML)
with open('urls.json','w') as fp:
    json.dump(hyperLinksPerHTML, fp)
#print(hyperLinksPerHTML)