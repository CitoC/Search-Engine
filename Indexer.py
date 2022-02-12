import json
from lib2to3.pgen2 import token
from bs4 import BeautifulSoup
import itertools
import re
from nltk.stem import PorterStemmer

class Index():
    def __init__(self):
        self.doc_id = {}            # associate each url with an id, e.g. {"https://ics.uci.edu": 1, "https://reddit.com": 2}
        self.current_id = 1         # increment each time after an id is associated with a document
        self.token_id = {}          # associate each token with the document where it appears, e.g. {"anteater": [1], "zot": [1,4]}
        self.tokens = []
        self.occurences = {}
        


    # this function expects the name of a file as a string. it will attempt to open the file and 
    # use the json library to extract the content attribute from the json file. Lastly, it will
    # send the content of the file as a string to the tokenize function to have it return the list 
    # of tokens. the list returned from tokenize is immediately returned by this function as well.
    # Additionally, it will also call assign_ID()
    def extract_content(self, file: str) -> list:
        try:
            # read from a json file
            with open(file, 'r') as f:
                # extract content from json files
                data = json.load(f)
        except: 
            print("Could not open JSON file..!")
            
        # assign url to an id
        self.assign_ID(data['url'])

        # return a list of words including stop words
        return self.tokenize(data['content'])

    # This function is called by extract_content() only. It will assign the url to a unique id.
    # The key/value pair is then added to doc_id dictionary.
    # example, {"https://ics.uci.edu": 1}
    def assign_ID(self, url: str):
        # checks to make sure that the url is not in the dictionary, if it is do nothing
        # if it is not add it into the dictionary.
        if url not in self.doc_id:
            # Updates the dictionary with the url and assigns it an id
            self.doc_id.update({url: self.current_id})
            # Updates the current id
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
        
        tokens.append(self.parse_tags(soup, important_tags))
        tokens.append(self.parse_tags(soup, relevant_tags))
        # perform cleanup on our tokens
        for i, list in enumerate(tokens):
            for j, text in enumerate(list):

                # first combinate any contractions by removing apostrophes
                p = re.compile('[’\']')
                tokens[i][j] = p.sub('', text)

                # then replace any character that isn't a number or letter with a space
                p = re.compile('[^a-zA-Z0-9]')
                tokens[i][j] = p.sub(' ', tokens[i][j])
                
                # lastly, remove any remaining extra spaces
                tokens[i][j] = re.sub(' +', ' ', tokens[i][j])

                # remove any leading and trailing spaces
                tokens[i][j] = tokens[i][j].strip()

                # remove any empty tokens
                if len(tokens[i][j]) == 0:
                    tokens[i].remove(tokens[i][j])

                # either add a new token to the list, or increment its counter
                if tokens[i][j].lower() in self.occurences.keys():
                    self.occurences[tokens[i][j].lower()] += 1
                else:
                    self.occurences[tokens[i][j].lower()] = 1

        # print(self.occurences)
        return tokens

    # this function takes a list to token and stem them, i.e., turns the tokens into their simplest form
    # example, "swimming" to "swim"
    # return a list of stemmed tokens
    def stem(self, token_list: list) -> list:
        stemmed_list = []
        ps = PorterStemmer()
        for lists in token_list:
            for token in lists:
                stemmed_list.append(ps.stem(token))
        return stemmed_list
    

    def create_pair(self, stem_list: list):
            for i,token in enumerate(stem_list):
                if token in self.token_id:
                    self.token_id[stem_list[i]].add(self.current_id - 1)    # subtracting 1 is needed to get the correct document id, since curren_id is incremented by 1 in assign_ID
                else:
                    self.token_id[stem_list[i]] = {self.current_id - 1}

    def create_index(self):
        with open('index.txt', 'w', encoding='utf-8') as file:
            for token in self.token_id:
                file.write(token + '\t')                       # print the key
                for id in self.token_id[token]:         # print postings
                    file.write(str(id) + ' ')
                file.write('\n')


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