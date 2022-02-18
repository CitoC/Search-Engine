from lib2to3.pgen2 import token
from Indexer import Index
import os

def my_debug(index: Index):
    print("------------Posting for this file------------")
    print(index.token_posting)
    print("---------------------------------------------")
    # print(index.occurrences)

def run():
    # a loop going over all the files in DEV need to happen here
    # this is just an example
    index = Index()
    directory = 'testdir'

    #Gets all of the folders in the Dev folder
    #This will extract the data from the Dev folder containing all the content we will look at. 
    for strfile in os.scandir(directory):
        #for each of the folders we will then go through them to get the json files
        for root, dirs, files in os.walk(strfile.path):
            print(strfile.path)
            #we will then extract the json content here
            for file in files:
                print(file)
                # call extract content on the json here. 
                path_of_json = strfile.path + '/' + file
                # indexing starts here
                token_list = index.extract_content(path_of_json)
                stem_list = index.stem(token_list)
                index.create_posting(stem_list)

                ### debugging ###
                # print("------------Posting for this file------------")
                print("------------Token List for this file------------")
                print(token_list)
                print("------------Stem List for this file------------")
                print(stem_list)
                # print(index.token_posting)
                # print("---------------------------------------------")
            # index.create_index()
                del token_list
                del stem_list

if __name__ == '__main__':
    run()

