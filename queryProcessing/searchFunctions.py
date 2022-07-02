def rankBySecondElem(list):
    """
    Helper function to be used in cosineSimRanking.
    :param list: list of the form [[docid1, rankingScore1], [docod2, rankingScore2]...
    :return: Sorted list by second entry.
    """
    return list[1]


def cosineSimRanking(intrestedPhrase, relevantDocs, invertedIndex, intersectinglist):
    """
    Ranks preform cosine similarity ranking.
    :param intrestedPhrase: User query must be preprocessed as a list of words
    :param relevantDocs: Hash table of document information
    :return: Sorted rank list with entries [docid, cosine similarity score].
    """
    rankedList = []
    print(intersectinglist)
    for key, value in relevantDocs.items():
        normalization = 1 / sqrt(value['doc vec length'])
        summationList = []
        if key in intersectinglist:
            for word in intrestedPhrase:
                summationList.append([num[3] for num in invertedIndex[word]['link'] if num[0] == key])
            # flatten summationList, then sum numbers
            vecSum = sum([num for numArr in summationList for num in numArr])
            rankingScore = normalization * (1 / sqrt(len(intrestedPhrase)) * vecSum)
            rankedList.append([key, rankingScore])
    return sorted(rankedList, key=rankBySecondElem, reverse=True)


def phrasalSearch(query, invertedIndex, docTable):
    """
    Preform phrasalSearch.
    :param query: Search query.
    :param invertedIndex: Inverted index
    :param docTable: Document table.
    :return: List of lists, by correlationg rank.
    """
    query = query[1:len(query) - 1].lower().strip().split()

    if checkIndex(query, invertedIndex):
        if len(query) == 1:
            return booleanSearch(''.join(query), invertedIndex, docTable)
        else:
            # multiple words in phrasal search, first we find relevant documents
            relevantDocsTemp = []
            toBeCleaned = []
            for word in query:
                # Get intersecting document set first, these are the only important docs
                relevantDocsTemp.append([entry[0] for entry in invertedIndex[word]['link']])
                toBeCleaned.append([[entry[0], entry[2], entry[3], word] for entry in invertedIndex[word]['link']])
            intersectingDocs = set(relevantDocsTemp[0])
            for doc in relevantDocsTemp:
                intersectingDocs = intersectingDocs & set(doc)
            intersectingDocs = list(intersectingDocs)  # documents containing all words in query

            # From using the idea of dictionaries within dictionaries to get positions easily.
            positionalDictionary = {}
            for entry in sum(toBeCleaned, []):
                if entry[0] not in positionalDictionary:
                    positionalDictionary[entry[0]] = {
                        'word': {entry[3]: entry[1]}
                    }
                elif entry[3] not in positionalDictionary[entry[0]]['word']:
                    positionalDictionary[entry[0]]['word'].update({entry[3]: entry[1]})
            finalDocs = []
            print("intersecting docs here ---------------")
            print(intersectingDocs)

            for entry in intersectingDocs:
                for num in range(0, len(query) - 1):
                    startArr = positionalDictionary[entry]['word'][query[num]]
                    inNextArr = any(item in list(map(lambda x: x + 1, startArr)) \
                                    for item in positionalDictionary[entry]['word'][query[num + 1]])
                    if not inNextArr:
                        break
                    finalDocs.append((entry))
            # only calculate cosine for relevant documents
            return cosineSimRanking(query, docTable, invertedIndex, finalDocs)
    else:
        return "Last entry not valid."



def booleanSearch(query, invertedIndex, docTable):
    if type(query) != list():
        query = query.split()

    if checkIndex(query, invertedIndex):
        if "and" in query:
            relevantDocsTemp = []
            toBeCleaned = []
            print("Conducting AND query...")
            # Get intersecting document set first
            for word in query:
                if word != "and":
                    relevantDocsTemp.append([entry[0] for entry in invertedIndex[word]['link']])
                    toBeCleaned.append([[entry[0], entry[3]] for entry in invertedIndex[word]['link']])
            intersectingDocs = set(relevantDocsTemp[0])
            for doc in relevantDocsTemp:
                intersectingDocs = intersectingDocs & set(doc)
            intersectingDocs = list(intersectingDocs)

            finalOutWithRanking = {}
            for entry in sum(toBeCleaned, []):
                if entry[0] not in finalOutWithRanking:
                    if entry[0] in intersectingDocs:
                        finalOutWithRanking[entry[0]] = entry[1]
                else:
                    finalOutWithRanking[entry[0]] += entry[1]
            return list(map(list, sorted(list(finalOutWithRanking.items()), key=rankBySecondElem, reverse=True)))
        elif "but" in query:
            relevantDocsTemp = []
            removingDocs = []
            print("Conducting BUT query...")

            locationOfBut = query.index("but")
            leftSideOfQuery = query[:locationOfBut]
            rightideOfQuery = query[locationOfBut + 1:]

            # Get documents that must be in INCLUDED
            for word in leftSideOfQuery:
                relevantDocsTemp.append([[entry[0], entry[3]] for entry in invertedIndex[word]['link']])
            relevantDocsTemp = sum(relevantDocsTemp, [])

            # Get documents that must be REMOVED
            for word in rightideOfQuery:
                removingDocs.append([entry[0] for entry in invertedIndex[word]['link']])
            removingDocs = sum(removingDocs, [])
            relevantDocs = [finalDocs for finalDocs in relevantDocsTemp if finalDocs[0] not in removingDocs]

            # final Ranking
            finalOutWithRanking = {}
            for entry in relevantDocs:
                if entry[0] not in finalOutWithRanking:
                    finalOutWithRanking[entry[0]] = entry[1]
                else:
                    finalOutWithRanking[entry[0]] += entry[1]
            # Note, dictionary was converted into a list of tuples, the finally a list of lists. This is done
            # in order to ensure consistency with the output in phrasal search.
            return list(map(list, sorted(list(finalOutWithRanking.items()), key=rankBySecondElem, reverse=True)))
        else:
            print("Conducting OR query...")
            relevantDocsTemp = []
            for word in query:
                if word != "or":
                    relevantDocsTemp.append([[entry[0], entry[3]] for entry in invertedIndex[word]['link']])
            relevantDocsTemp = sum(relevantDocsTemp, [])  # flatten a 2d array
            relevantDocs = {}  # using dictionary for ease of merging and updating correlations
            for entry in relevantDocsTemp:
                if entry[0] not in relevantDocs:
                    relevantDocs[entry[0]] = entry[1]
                else:
                    relevantDocs[entry[0]] += entry[1]
            # Note, dictionary was converted into a list of tuples, the finally a list of lists. This is done
            # in order to ensure consistency with the output in phrasal search.
            return list(map(list, sorted(list(relevantDocs.items()), key=rankBySecondElem, reverse=True)))
    else:
        return "Your word is not in the inverted index."


def checkIndex(query, invertedIndex):
    """
    Implementing early stop. Check if query words are in inverted index or not.
    :param query:
    :param invertedIndex:
    :return: True if words can be found, false otherwise.
    """
    for word in query:
        if word != "and" or word != "or" or word != "but":
            if word not in invertedIndex:
                print(word + " not a valid entry")
                return False
    return True


def webSearch(invertedIndex, docTable):
    """
    Web engine console.
    :param invertedIndex: Inverted index table.
    :param docTable: Table containing doc information
    :return:
    """
    print("Now the search beings:")
    searchEntry = input("enter a search key=>")
    while (searchEntry != ""):
        # Check for phrasal first.
        if "\"" in searchEntry:
            print("Preforming phrasal search...")
            print(phrasalSearch(searchEntry, invertedIndex, docTable))
        elif len(searchEntry.split()) == 1:
            print("Only searching for one word...")
            print(booleanSearch(searchEntry, invertedIndex, docTable))
        else:
            print("Preforming boolean search...")
            print(booleanSearch(searchEntry, invertedIndex, docTable))
        searchEntry = input("enter a search key=>")
    print("Bye")
