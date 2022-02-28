from lib2to3.pgen2 import token
from Indexer import Index
import os
import psutil
import subprocess

# this function is meant to handle offloading of memory into disk. It expects a float for previous_memory_usage
# to compare against the threshold_offset set in the main function.
# the other parameters (index, token_list, stem_list) are simply used to delete as much memory as possible from
# RAM after writing to disk. this function will use a bash command, sort, to sort the resulting partial index
# file in alphabetical order.
# this function will either return the previous_memory_usage that it received if the threshold wasn't met, or
# if a partial index is made, then it will set the previous_memory_usage to the new threshold that it just met
# (to set a new threshold for the next partial index)
def handle_ram_threshold(folder_count:int, index: Index, token_list: list) -> None:
    # when we hit the RAM threshold
   # if psutil.virtual_memory()[2] > previous_memory_usage + threshold_offset:
   if folder_count % 30 == 0:
        # set a new previous 
        #previous_memory_usage = psutil.virtual_memory()[2]

        # create a partial index
        file_name = index.create_index()

        # sort the partial index by using the 'sort' bash command
        bash_command = 'sort ' + file_name + ' -o ' + file_name
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        # try to delete as much from memory as possible
        del index
        del token_list

        # create a new partial index
        index = Index()

    #return previous_memory_usage

def main():
    index = Index()
    directory = 'DEV'
    threshold_offset = 5
    previous_memory_usage = psutil.virtual_memory()[2]
    folder_count = 0

    #Gets all of the folders in the Dev folder
    #This will extract the data from the Dev folder containing all the content we will look at. 
    for strfile in os.scandir(directory):
        #for each of the folders we will then go through them to get the json files
        for root, dirs, files in os.walk(strfile.path):
            folder_count += 1
            
            #we will then extract the json content here
            for file in files:
                
                path_of_json = strfile.path + '/' + file
                print(path_of_json)
                # indexing starts here
                token_list = index.extract_content(path_of_json)
                index.create_posting(token_list)

                # after each file, check if the RAM threshold has been reached
                #handle_ram_threshold(previous_memory_usage, threshold_offset, index, token_list)

            handle_ram_threshold(folder_count, index, token_list)  


    handle_ram_threshold(90, index, token_list)       
        
if __name__ == '__main__': main()