##################################################################################################
# Created By: Srikanth Akiti, Sonya Cirlos, Jose Ruben Espinoza, Marlon Martinez, Albert Trevino #
# Project Title: Web Search Project                                                              #
# Date Range: Summer I 2022                                                                      #
# Short Description: This is the file used for the crawlers what will be allowed for others to use#
##################################################################################################


from bs4 import BeautifulSoup

import os
import queue
from robot import *


class Spider:

    #variables used among class instances
    directory_name = ""
    start_url = " "
    domain_name = ""
    queue_file = ""
    crawled_file = ""
    q = set()
    crawled = set()

    @staticmethod
    def crawlerchecker(url):
        print("Adding to the list of visited sites currently adding: ", url)
        if url not in crawled:
            Spider.crawled.add(url)


    @staticmethod
    def starterlist(url):
        print("start adding to the queue, all the links that have been found so they can be visited")
        if url not in q:
            q.append(url)


    @staticmethod
    def addlinks(links):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.directory_name not in url:
                continue
            Spider.queue.add(url)


    @staticmethod
    def update_files():
        print("update files: ")
