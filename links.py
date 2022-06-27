from html.parser import HTMLParser
from urllib import parse

class Links(HTMLParser):

    def __init__(self, url, page_url):
        super().__init()
        self.url = url
        self.page_url = page_url
        self.links = set()

    #this will help remove all the href tags so we can just get the links of every document
    def tag(self,tag,attrs):
        if tag == 'a':
            for(attribute,value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.url,value) # this will join the whole url link and then will be stored to the set
                    self.links.add(url)

    def pagelinks(self):
        return self.links

    def error(self, message):
        print("ERROR OCCURED IN LINKS: ")
        pass