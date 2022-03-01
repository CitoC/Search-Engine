import json
from lib2to3.pgen2 import token
import string
from bs4 import BeautifulSoup
import itertools
import re
from nltk.stem import PorterStemmer
import glob
from contextlib import ExitStack
import subprocess

class Index():
    def __init__(self):
        self.doc_id = {}            # associate each url with an id, e.g. {"https://ics.uci.edu": 1, "https://reddit.com": 2}
        self.current_id = 1         # increment each time after an id is associated with a document
        self.token_posting = {}     # associate each token with the document where it appears, e.g. {"anteater": [(1,3),(5,2)], "zot": [(1,4)]}
        self.tokens = []
        self.file_num = 0
        self.occurrences = {}

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
            self.doc_id.update({self.current_id: url})
            # Updates the current id
            self.current_id = self.current_id + 1 
       
    # this function uses BeautifulSoup to parse the content attribute of the JSON file.
    # this function will return a 2D list of tokens; element 0 will contain a list of phrases
    # that are considered important text and element 1 will contain individual words found
    # within less important tags, such as <p> and <li>
    def tokenize(self, content: str) -> list:
        tokens = []
        self.occurrences = {}        # reset the occurences dictionary

        # create a BS object to parse content attribute from JSON file
        soup = BeautifulSoup(content, "html.parser")

        # the different tags we will use to parse text from each page's contents
        important_tags = ['meta', 'b', 'strong', 'header', 'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        relevant_tags = ['p', 'li']
        
        #Turns the returned sets into lists to process them
        tokens.append(self.parse_tags(soup, important_tags))
        tokens.append(self.parse_tags(soup, relevant_tags))

        # print(self.occurrences)
        return tokens

    # this function takes a list to token and stem them, i.e., turns the tokens into their simplest form
    # example, "swimming" to "swim"
    # return a list of stemmed tokens
    ''' # DEFUNT #
    def stem(self, token_list: list) -> list:
        stemmed_list = []
        ps = PorterStemmer()
        for lists in token_list:
            for token in lists:
                stemmed_list.append(ps.stem(token))
        return stemmed_list
    ''' 
    # create posting for the token
    # example, {“anteater”: [(1,3),(5,2)], “zot”: [(3,6)]}
    def create_posting(self, token_list: list):
            id = self.current_id - 1
            # REMINDER: mixing important list and normal list. Fix later
            for l in token_list:
                for token in l:
                    # if token is already in the posting
                    if token in self.token_posting.keys():
                        self.token_posting[token].append(tuple([id, self.occurrences[token]])) # subtracting 1 is needed to get the correct document id, since curren_id is incremented by 1 in assign_ID
                    else:
                        self.token_posting[token] = [tuple([id, self.occurrences[token]])]

    def create_index(self) -> str:
        tName = './indexes/index'
        fName = '%s%d.txt' % (tName, self.file_num)
        with open(fName, 'w', encoding='utf-8') as file:
            for token in self.token_posting.keys():
                file.write(token + '\t')                # print the key
                for item in self.token_posting[token]:
                    file.write('(' + str(item[0]) + ',' + str(item[1]) + ') ')
                file.write('\n')
        
        # increment file number
        self.file_num += 1
        # empty 
        self.token_posting = {}

        # return the file name for sorting of file
        return fName

    def parse_tags(self, soup: BeautifulSoup, tag_list: list,) -> set:
        tokens = []

        for tag in tag_list:
            # find all of the following tags
            results = soup.find_all(tag)
            
            # parse each result 
            for result in results:

                # this list will temporarily store the tokens found in the current result from the
                # soup.find_all function call to be checked against a frequency map and added to
                # a tokens set
                temp_tokens = []

                if tag == 'meta':
                    # filter out only the important meta tags such as the page's description and author(s)
                    if 'name' in result.attrs.keys() and (result.attrs['name'] == 'description' or result.attrs['name'] == 'author'):
                        if 'content' in result.attrs.keys():
                            temp_tokens.append(result.attrs['content'])
                # split normal tags into separate words
                elif tag == 'p' or tag == 'li':
                    temp_tokens = result.text.split()
                # treat the entire "important text" phrase as a token
                else:
                    temp_tokens.append(result.text)

                # perform cleanup on our tokens
                temp_tokens = self.token_clean_up(temp_tokens)
                ps = PorterStemmer()                # imported stemmer to let occurences contain stemmed tokens
                stem_tokens = [ps.stem(t) for t in temp_tokens]
                for t in stem_tokens:
                    # either add a new token to the list, or increment its counter
                    if t in self.occurrences.keys():
                        self.occurrences[t] += 1
                    else:
                        self.occurrences[t] = 1
                        tokens.append(t)

        return tokens      

    # this function will aid in clean-up of tokens by removing any non-alphanumeric characters
    def token_clean_up(self, tokens):
        for i, text in enumerate(tokens):
            # first combinate any contractions by removing apostrophes
            p = re.compile('[’\']')
            tokens[i] = p.sub('', tokens[i])

            # then replace any character that isn't a number or letter with a space
            p = re.compile('[^a-zA-Z0-9]')
            tokens[i] = p.sub(' ', tokens[i])
            
            p = re.compile(' +')
            # lastly, remove any remaining extra spaces
            tokens[i] = p.sub(' ', tokens[i])

            # remove any leading and trailing spaces
            tokens[i] = tokens[i].strip()

        # delete empty tokens
        tokens = list(filter(None, tokens))

        return tokens

    # this function will locate every partial index and then combine them all to create
    # a single index with all of the tokens sorted in alphabetical order first, and each
    # token's doc_ids sorted in ascending order
    def merge_partial_indexes(self):
        # find all partial indexes within the indexes directory
        #partial_indexes = glob.glob('indexes/index*.txt')
        partial_indexes = glob.glob('indexes/index*.txt')

        # output file to write to
        f_output = open("index.txt", "w")
        
        # open an input buffer for each partial index
        with ExitStack() as stack:
            files = [stack.enter_context(open(fname)) for fname in partial_indexes]

            lines = []
            done = True

            # read a line from each open file
            for file in files:
                lines.append(file.readline())

            # check if any of the lines have text to parse
            for line in lines:
                # if at least one line has text, then we must not be done
                if line:
                    done = False
                    break
            else:
                done = True

            # while at least one file still has a line to read
            while (not done):
                first_index = 0
                while first_index < len(lines) and not lines[first_index]:
                    first_index += 1
                

                # determine which line's token comes first (alphabetically)
                for i, line in enumerate(lines):
                    # always compare the current line with the previous first line (alphabetically)
                    if lines[i] and lines[i] < lines[first_index]:
                        first_index = i

                same_line_indexes = []
                first_token = ''

                # get just the token of the leading line
                for i, char in enumerate(lines[first_index]):
                    if char == '(':
                        first_token = lines[first_index][0:i-1]
                        break

                # check if any other line contains the same token
                for i, line in enumerate(lines):
                    # ignore the smallest
                    # if i != first_index:
                    # get just the token of the current line
                    for j, char in enumerate(lines[i]):
                        if char == '(':
                            token = lines[first_index][0:j-1]
                            break
                    else:
                        token = ''
                    
                    if token == first_token:
                        same_line_indexes.append(i)

                # if there at least a matching token
                if len(same_line_indexes) > 1:

                    doc_ids = []
                    # parse each token's doc_ids/frequencies
                    for index in same_line_indexes:
                        doc_id, frequency = self.parse_line(lines[index])
                        for i, _ in enumerate(doc_id):
                            doc_ids.append((doc_id[i], frequency[i]))

                    # sort the doc_ids in ascending order
                    doc_ids = sorted(doc_ids, key = lambda X: X[0])
                    
                    f_output.write(token + '\t')
                    i = 0
                    # these nested loops use a 2 pointer approach to find all matching
                    # doc ids and sum their frequencies for merging into a single pair
                    while i < len(doc_ids):
                        sum = 0
                        j = i
                        while (j < len(doc_ids) and doc_ids[i][0] == doc_ids[j][0]):
                            sum += int(doc_ids[j][1])
                            j += 1
                        f_output.write('(' + str(doc_ids[i][0]) + ',' + str(sum) + ') ')
                        i = j
                    
                    f_output.write('\n')

                    # empty every line from this section to remove it from next iteration
                    for i in same_line_indexes:
                        lines[i] = ''
                else:
                    # write the line that comes first to file
                    f_output.write(lines[first_index])

                    # empty the current line to remove it from next iteration
                    lines[first_index] = ''

                # read a line from each open file
                for i, file in enumerate(files):
                    if not lines[i]:
                        lines[i] = file.readline()

                # check if any of the lines have text to parse
                for line in lines:
                    # if at least one line has text, then we must not be done
                    if line:
                        done = False
                        break
                else:
                    done = True

            # delete all partial indexes from the indexes directory
            bash_command = 'rm indexes/*'
            process = subprocess.Popen(bash_command, shell=True, stdout=subprocess.PIPE)
            output, error = process.communicate()

        f_output.close()

        # move the new complete index from the base directory (of this project) into indexes/
        bash_command = 'mv index.txt indexes/'
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    #this function will parse the line of the file to get the 
    #doc ids from the line
    def parse_line(self, line:string):
        tokens = line.split()
        doc_id = []
        token_occurrences = []
        #Gets the numbers of the ids that relate to the tokem 
        
        start_of_doc_ids = 0

        # find where the pairs begin
        for i, token in enumerate(tokens):
            if token[0] == '(':
                start_of_doc_ids = i
                break

        # trim the tokens to start at the document ids
        tokens = tokens[start_of_doc_ids:]

        # for each pair of (document_id,occurrences)
        for pair in tokens:
            # check each char of the pair
            for i, char in enumerate(pair):
                # find the comma
                if char == ',':
                    # append the left side of the comma to the list of doc_ids
                    doc_id.append(pair[1:i])
                    # the right side to the list of occurrences
                    token_occurrences.append(pair[i+1:-1])
                    break

        return doc_id, token_occurrences


    #This function will read in the input and tokenize the input for retrieval
    #of the document in the index
    #Only need to test the querys (cristina lopes, machine learning, ACM, master of software engineering)
    def get_input(self, input:str):
        pass

    #this function will go through the index and retrieve the relevant 
    #documents releated to the query
    #the majority of milestone 2 will probably be involved here(might need more functions to help the processing)
    # returns a list of the relevent documents to compare
    def retrieve_relevant_document(self):
        pass

    #this function will load in one of the index files into the index in memory
    def load_index_from_file(self):
        pass

    #this function will clear the index
    def clear_index(self):
        pass
    
    #this function will output the most relevant document to the console
    def output_document(self):
        pass