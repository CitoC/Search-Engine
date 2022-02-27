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



document_urls = {}

def map_documents():
    document_id = 0
    directory = 'DEV'
    #Gets all of the folders in the Dev folder
    #This will extract the data from the Dev folder containing all the content we will look at. 
    for strfile in os.scandir(directory):
        #for each of the folders we will then go through them to get the json files
        for root, dirs, files in os.walk(strfile.path):
            print(strfile.path)
            #we will then extract the json content here
            for file in files:
                path_of_json = strfile.path + '/' + file
                try:
                    # read from a json file
                    with open(path_of_json, 'r') as f:
                        # extract content from json files
                        data = json.load(f)
                except: 
                    print("Could not open JSON file..!")
                   
                document_urls[document_id] = data['url']
                document_id += 1


def main():
    map_documents()
    test = Query()
    while True:
        user_input = test.get_input()
        if user_input == '-1': break

        test.retrieve_relevant_document('/Users/joshuamontellano/Desktop/cs121/Search-Engine/indexes/index83.txt')
        # test.print_id()
        #intersections = test.find_intersection()

        sorted_intersections = test.highest_tf_idf_scores()
        #sorted_intersections = test.rank_urls(intersections)

        for i in range(5):
            # print(sorted_intersections[i], end=' ')
            print(document_urls[int(sorted_intersections[i])])
        print('')

        del test
        test = Query()

if __name__ == '__main__': main()