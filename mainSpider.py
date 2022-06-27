import threading
from queue import Queue
from Spider import Spider
from domains import *
from filecreat import *
import time

PROJECT_NAME = 'netfunny'
# need to find a way to pass in the rhf folder to start the index at the local folder

# start by checking out directory
directory = format(os.getcwd())
# then we change it to the directory we need
os.chdir(directory + "/rhf/rhf")
# print to see out new current working directory
print("CURRENT DIRECTORY", os.getcwd())
directory = os.getcwd()
# this prints out all the files in the cheDoc
directoryList = os.listdir(directory)
print("DIRECTORY LIST OF RHF: ", directoryList)
#C:\Users\marlo\PycharmProjects\searchEngine\rhf\rhf\index.html

for file in directoryList:
    if file  == "index.html":
        test = file

print("SHOULD BE MY INDEX: ", test)


HOMEPAGE = test

print("HOMEPAGE IS: " + HOMEPAGE)

DOMAIN_NAME = domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
time.sleep(10)

print(DOMAIN_NAME, "index is htis aneasd asdf asd fasdf ")

#Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_workers()
crawl()
