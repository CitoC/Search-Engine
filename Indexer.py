import json
from lib2to3.pgen2 import token
from bs4 import BeautifulSoup
import itertools

class Index():
    def __init__(self):
        self.doc_id = {}            # associate each url with an id, e.g. {"https://ics.uci.edu": 1, "https://reddit.com": 2}
        self.current_id = 1         # increment each time after an id is associated with a document
        self.token_id = {}          # associate each token with the document where it appears, e.g. {"anteater": [1], "zot": [1,4]}
                                    # this is a list of tuples

    # this function expects the name of a file as a string. it will attempt to open the file and 
    # use the json library to extract the content attribute from the json file. Lastly, it will
    # send the content of the file as a string to the tokenize function to have it return the list 
    # of tokens. the list returned from tokenize     is immediately returned by this function as well.
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

    def assign_ID(self, url):
        # assign a url with a unique id
        # add to the doc_id dictionary
        # example, {"https://ics.uci.edu": 1}
        # doesn't return anything but modify the doc_id itself

        #checks to make sure that the url is not in the dictionary, if it is do nothing
        #if it is not add it into the dictionary.
        if url not in self.doc_id:

            #Updates the dictionary with the url and assigns it an id
            self.doc_id.update({url: self.current_id})
            #Updates the current id
            self.current_id = self.current_id + 1 
       
    # this function uses BeautifulSoup to parse the content attribute of the JSON file.
    # this function will return a 2D list of tokens; element 0 will contain a list of phrases
    # that are considered important text and element 1 will contain individual words found
    # within less important tags, such as <p> and <li>
    def tokenize(self, content: str) -> list:
        tokens = []

        # create a BS object to parse content attribute from JSON file
        soup = BeautifulSoup(content, "html.parser")

        # the different tags we will use to parse text from each page's contents
        important_tags = ['meta', 'b', 'strong', 'header', 'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        relevant_tags = ['p', 'li']
        # <header> might not be a good idea... if we keep it, it will need to be 
        # tokenized further to remove tabs and newlines
        
        tokens.append(self.parse_tags(soup, important_tags))
        tokens.append(self.parse_tags(soup, relevant_tags))

        return tokens

    def stem(self):
        # stem the words, i.e., turns the tokens into their simplest form
        # example, "swimming" to "swim"
        # return a list of stemmed tokens
        return 0
    
    def create_pair_file(self):
        # NOT SURE ABOUT THIS
        # write to a file each current_id
        # example, anteater 1\nzot 4\nzot 
        return 0

    def create_index_file(self):
        # NOT SURE ABOUT THIS
        # create an index file using the file that is created by add_pair_to_file
        # go through every element in token_id and write to a file
        return 0

    def parse_tags(self, soup: BeautifulSoup, tag_list: list) -> list:
        tokens = []

        for tag in tag_list:
            # find all of the following tags
            results = soup.find_all(tag)
            
            # parse each result 
            for result in results:
                if tag == 'meta':
                    # filter out only the important meta tags such as the page's description and author(s)
                    if 'name' in result.attrs.keys() and (result.attrs['name'] == 'description' or result.attrs['name'] == 'author'):
                        tokens.append(result.attrs['content'])
                # split normal tags into separate words
                elif tag == 'p' or tag == 'li':
                    tokens.append(result.text.split()) 
                # treat the entire "important text" phrase as a token
                else:
                    tokens.append(result.text)
        
        # since each result returns a list of tokens, the resulting token list becomes 2 dimensional.
        # here we use itertools to merge the lists into a single large list of all the tokens found
        # within the <p> and <li> tags
        if tag_list[0] == 'p':
            return list(itertools.chain.from_iterable(tokens))
        else: # return the list of "important text" phrases
            return tokens