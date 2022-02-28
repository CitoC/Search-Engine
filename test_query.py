from Query import Query
from lib2to3.pgen2 import token
from Indexer import Index
import os
import psutil
import subprocess
import json
from lib2to3.pgen2 import token
import string
from bs4 import BeautifulSoup
import itertools
import re
from nltk.stem import PorterStemmer



def main():
    test = Query()
    test.get_doc_url('documentIDs.txt')
    while True:
        user_input = test.get_input()
        if user_input == '-1': break

        test.retrieve_relevant_document('/mnt/c/Users/serom/Documents/School/Winter 2022/CS 121/Assignment 3/Search-Engine/indexes/index83.txt')
        # test.print_id()
        intersections = test.find_intersection()

        sorted_intersections = test.rank_urls(intersections)

        for i in range(5):
            # print(sorted_intersections[i], end=' ')
            print(document_urls[sorted_intersections[i]])
        print('')

        del test
        test = Query()

if __name__ == '__main__': main()