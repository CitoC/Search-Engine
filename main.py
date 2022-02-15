from lib2to3.pgen2 import token
from Indexer import Index
import os

def run():
    # a loop going over all the files in DEV need to happen here
    # this is just an example
    index = Index()
    directory = 'DEV'

    #Gets all of the folders in the Dev folder
    #This will extract the data from the Dev folder containing all the content we will look at. 
    for strfile in os.scandir(directory):
        #for each of the folders we will then go through them to get the json files
        for root, dirs, files in os.walk(strfile.path):
            print(strfile.path)
            #we will then extract the json content here
            for file in files:
                print(file)
                #call extract content on the json here. 
                path_of_json = strfile.path + '/' + file
                # indexing starts here
                token_list = index.extract_content(path_of_json)
                stem_list = index.stem(token_list)
                index.create_pair(stem_list)
            index.create_index()

if __name__ == '__main__':
    run()
