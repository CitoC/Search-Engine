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
    # read document ids from disk to memory
    doc_id = test.get_doc_url('documentIDs.txt')

    while True:
        user_input = test.get_input()
        if user_input == '-1': break # stop condition

        test.retrieve_relevant_document('indexes/index83.txt')
        # test.print_id()
        #intersections = test.find_intersection()

        sorted_intersections = test.highest_tf_idf_scores()
        #sorted_intersections = test.rank_urls(intersections)

        try:
            for i in range(5):
                print(doc_id[sorted_intersections[i]])
            print('')
        except:
            print("Too bad, what you are finding does not exist in the Corpus!")

        del test
        test = Query()

if __name__ == '__main__': main()