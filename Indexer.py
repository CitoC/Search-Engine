import json
import nltk
from nltk.tokenize import RegexpTokenizer

class Index():
    def __init__(self):
        self.doc_id = {}            # associate each url with an id, e.g. {"https://ics.uci.edu": 1, "https://reddit.com": 2}
        self.current_id = 1         # increment each time after an id is associated with a document
        self.token_id = {}          # associate each token with the document where it appears, e.g. {"anteater": [1], "zot": [1,4]}
                                    # this is a list of tuples

    # this function expects the name of a file as a string. it will attempt to open the file and 
    # use the json library to extract the content attribute from the json file. Lastly, it will
    # send the content of the file as a string to the tokenize function to have it return the list 
    # of tokens. the list returned from tokenize is immediately returned by this function as well.
    def extract_content(self, file: str) -> list:
        try:
            # read from a json file
            with open(file, 'r') as f:
                # extract content from json files
                data = json.load(f)
                
                # return a list of words including stop words
                return self.tokenize(data['content'])
        except: 
            print("Could not open JSON file..!")

    def assign_ID():
        # assign a url with a unique id
        # add to the doc_id dictionary
        # example, {"https://ics.uci.edu": 1}
        # doesn't return anything but modify the doc_id itself
        return 0

    # this function uses the nltk library to tokenize only the alphanumeric sequences within the 
    # content string passed to it. this function returns a list with duplicate tokens 
    def tokenize(self, content: str) -> list:
        # normalize the words to token, e.g. U.S.A to USA, etc.
        nltk = RegexpTokenizer(r'\w+')
        
        # return a list of tokens
        return nltk.tokenize(content)

    def stem():
        # stem the words, i.e., turns the tokens into their simplest form
        # example, "swimming" to "swim"
        # return a list of stemmed tokens
        return 0
    
    def create_pair_file():
        # NOT SURE ABOUT THIS
        # write to a file each current_id
        # example, anteater 1\nzot 4\nzot 
        return 0

    def create_index_file():
        # NOT SURE ABOUT THIS
        # create an index file using the file that is created by add_pair_to_file
        # go through every element in token_id and write to a file
        return 0