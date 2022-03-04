import os
import json
from Indexer import Index

directory = 'DEV'
id = 1
index = Index()
doc_id = {}

# create (id, url) pair
for strfile in os.scandir(directory):
    for root, dirs, files in os.walk(strfile.path):
        print(strfile.path)
        for file in files:
            path = strfile.path + '/' + file
            with open(path, 'r') as f:
                data = json.load(f)
            url = data['url']
            doc_id.update({id: url})
            id = id + 1
           
# write everything to file
with open('document IDs.txt', 'w', encoding='utf-8') as file:
    for key in doc_id.keys():
        file.write(str(key) + ':' + str(doc_id[key] + '\n'))


# def assign_ID(self, url: str):
#     # checks to make sure that the url is not in the dictionary, if it is do nothing
#     # if it is not add it into the dictionary.
#     if url not in self.doc_id:
#         # Updates the dictionary with the url and assigns it an id
#         self.doc_id.update({self.current_id: url})
#         # Updates the current id
#         self.current_id = self.current_id + 1 

# def extract_content(self, file: str) -> list:
#     try:
#         # read from a json file
#         with open(file, 'r') as f:
#             # extract content from json files
#             data = json.load(f)
#     except: 
#         print("Could not open JSON file..!")
        
#     self.assign_ID(data['url'])