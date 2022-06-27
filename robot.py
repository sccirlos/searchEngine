##################################################################################################
# Created By: Srikanth Akiti, Sonya Cirlos, Jose Ruben Espinoza, Marlon Martinez, Albert Trevino #
# Project Title: Web Search Project                                                              #
# Date Range: Summer I 2022                                                                      #
# Short Description: This is the file used for the crawlers what will be allowed for others to use#
##################################################################################################

# Import necessary libraries

import threading
from queue import Queue
from domians import *
from Spider import Spider


# used to unzip the files from zipped folder
import queue
from zipfile import ZipFile

# helps with the parsing speed of XML files
import lxml

# this library helps with the http requests such as GET and POST
import requests

# help easily parse HTML and XML data
from bs4 import BeautifulSoup

# just a library I like using to testing out my code the sleep method to be more exact
import time
import os

URL = "https://www.netfunny.com/rhf/index.html"
DOMAINNAME =domain_name()




def createdirectory(directory):
    if not os.path.exist(directory):
        print("Creating Project: " + directory)
        os.makedirs(directory)

#queue to make sure crawler doesnt revisit same files
def datafiles(project_name, start_url):
    queue = project_name + 'queue.txt'
    crawled = project_name + 'crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, start_url)
    # crawled files for a waiting list, if it's the 1st time then we obviously start w no files so its empty
    if not os.path.isfile(crawled):
        write_file(crawled, '')


# this is to write data to the files of what we find
def write_file(path,data):
    f = open(path, 'w')
    f.write(data)
    f.close()


def addtofile(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


def deletefilecontent(path):
    with open(path, 'w'):
        pass

#read file and convert to a set
def fileset(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line)




def parse (response):
    print(response.text)

def listHtmls(htmldoc):
    print("inside crawler", htmldoc)
    name = htmldoc.find("meta")
    title = htmldoc.title
    print(name.text)
    print(title)
    parse(htmldoc)
    time.sleep(1)

if __name__ == '__main__':
    # start by checking out directory
    directory = format(os.getcwd())
    # then we change it to the directory we need
    os.chdir(directory + "/rhf/rhf")
    # print to see out new current working directory
    print("CURRENT DIRECTORY",os.getcwd())
    directory = os.getcwd()
    # this prints out all the files in the cheDoc
    directoryList = os.listdir(directory)

    # for all the files present in that
    # directory
    for filename in directoryList:
        print("FILENAME: ", filename)
        # check whether the file is having
        # the extension as html and it can
        # be done with endswith function
        if filename.endswith('.html') or filename.endswith('.htm'):
            # os.path.join() method in Python join
            # one or more path components which helps
            # to exactly get the file
            fname = os.path.join(directory, filename)
            #print("Current file name ..", os.path.abspath(fname))
            print(filename)
            #SHOULD PASS TO THE CRAWLER HERE SINCE FILE IS ACCEPTABLE

            # open the file
            with open(fname, 'r') as file:

                doc = BeautifulSoup(file.read(), 'html.parser')
                # function to seperate each file independently by the attritues
                listHtmls(doc)
                # parse the html as you wish
                for tag in doc.findAll(True):
                    print(tag.name, " : ", len(doc.find(tag.name).text))
               # tags = doc.find_all("p")
                #print(tags)
        else :
            #then we know that it might be a new directory or a link
            print("not html file it is: ", filename)
            #we need to traverse though these and find the index files of each file in there

    Spider.crawler()