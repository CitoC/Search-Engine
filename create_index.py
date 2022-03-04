from Indexer import Index
import os
import subprocess

# this function checks whether it is time to write a partial index to file. it currently
# uses the number of folders that have been explored to determine when to create a new
# partial index. the current implementation also tries to make a maximum of 3 partial indexes.
def create_partial_index(folder_count:int, index: Index, token_list: list) -> None:
   if folder_count % 30 == 0:
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

def main():
    index = Index()
    # directory = 'DEV'
    # folder_count = 0

    # #Gets all of the folders in the Dev folder
    # #This will extract the data from the Dev folder containing all the content we will look at. 
    # for strfile in os.scandir(directory):
    #     #for each of the folders we will then go through them to get the json files
    #     for _, _, files in os.walk(strfile.path):
    #         folder_count += 1
            
    #         #we will then extract the json content here
    #         for file in files:
    #             path_of_json = strfile.path + '/' + file
    #             print(path_of_json)
    #             # indexing starts here
    #             token_list = index.extract_content(path_of_json)
    #             index.create_posting(token_list)

    #         create_partial_index(folder_count, index, token_list)  

    # create_partial_index(30, index, token_list)       
    index.merge_partial_indexes()
        
if __name__ == '__main__': main()