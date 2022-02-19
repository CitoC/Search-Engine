from lib2to3.pgen2 import token
from Indexer import Index
import os
# import psutil
import subprocess

# this function is meant to handle offloading of memory into disk. It expects a float for previous_memory_usage
# to compare against the threshold_offset set in the main function.
# the other parameters (index, token_list, stem_list) are simply used to delete as much memory as possible from
# RAM after writing to disk. this function will use a bash command, sort, to sort the resulting partial index
# file in alphabetical order.
# this function will either return the previous_memory_usage that it received if the threshold wasn't met, or
# if a partial index is made, then it will set the previous_memory_usage to the new threshold that it just met
# (to set a new threshold for the next partial index)
# def handle_ram_threshold(previous_memory_usage: float, threshold_offset: int, index: Index, token_list: list, stem_list: list) -> float:
#     # when we hit the RAM threshold
#     if psutil.virtual_memory()[2] > previous_memory_usage + threshold_offset:
#         # set a new previous 
#         previous_memory_usage = psutil.virtual_memory()[2]

#         # create a partial index
#         file_name = index.create_index()

#         # sort the partial index by using the 'sort' bash command
#         bash_command = 'sort ' + file_name + ' -o ' + file_name
#         process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
#         output, error = process.communicate()

#         # try to delete as much from memory as possible
#         del index
#         del token_list
#         del stem_list

#         # create a new partial index
#         index = Index()

#     return previous_memory_usage

def my_debug(index: Index):
    print("------------Posting for this file------------")
    print(index.token_posting)
    print("---------------------------------------------")
    # print(index.occurrences)

def run():
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
                index.create_posting(token_list)

                ### debugging ###
                # print("------------Token List for this file------------")
                # print(token_list)
                # print("------------Stem List for this file------------")
                # print(stem_list)
            # index.create_index()
                del token_list
        
    print("------------Posting--------------------------")
    print(index.token_posting)
    print("---------------------------------------------")
if __name__ == '__main__':
    run()

