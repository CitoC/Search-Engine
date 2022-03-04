import string
from nltk.stem import PorterStemmer
import math
from collections import OrderedDict

class Query():
    def __init__(self):
        self.tokens_list = []
        self.token_documents = {}
        self.token_frequencies = {}
        self.doc_id = {}
        self.total_number_of_documents = 0
        self.token_tf_idf = {}
        self.table_of_contents = {}
        
    # This function will read in the input and tokenize the input for retrieval
    # of the document in the index
    def get_input(self):
        self.tokens_list = []
        self.token_documents = {}
        self.token_frequencies = {}
        self.token_tf_idf = {}

        # will split by white space to see get the tokens of the query that must be processed
        # should be simple for the queries for milestone 2 will need changes later on
        query = '' 
        while not query:
            query = input("Search: ")
            query = query.strip()
            tokens = query.split()
            for i in tokens:
                if not i.isalnum():
                    print('Alphanumeric characters only!')
                    query = ''
                    break

        tokens =  query.split()
        ps = PorterStemmer()

        # clear the previous tokens
        self.tokens_list = []

        for token in tokens:
            self.tokens_list.append(ps.stem(token))

        self.tokens_list = list(OrderedDict.fromkeys(self.tokens_list))
        
        return query

    # this function will go through the index and retrieve the relevant 
    # documents releated to the query
    def retrieve_relevant_document(self, file_name):
        if not self.tokens_list:
            return

        # sort the list of tokens
        self.tokens_list = sorted(self.tokens_list)

        # count the number of lines here for  total number of documnets
        with open(file_name, 'r') as file:
            # use the table of contents to seek to the proper letter
            ptr = 0
            file.seek(self.table_of_contents[self.tokens_list[ptr][0]])
            line = file.readline()
            # Goes through the file line by line 
            while line and ptr < len(self.tokens_list):
                #checks to see if the token is in that line 
                # If the token is in the line find its elements
                if self.tokens_list[ptr]  + '\t' == line[0:len(self.tokens_list[ptr]) + 1]:
                    doc_ids, token_occurrences = self.parse_line(line)
                    self.token_documents.update({self.tokens_list[ptr]: doc_ids})
                    self.token_frequencies.update({self.tokens_list[ptr]: token_occurrences})

                    for i, doc_id in enumerate(doc_ids):
                        # Calculates the tf-idf score of the token at the document_id and occurence 
                        tf_idf_score = (1 + math.log(float(token_occurrences[i]))) * math.log(len(self.doc_id) / len(self.token_documents[self.tokens_list[ptr]]) )

                        # Checks to see if the token is already present in the token_tf_idf map
                        if self.tokens_list[ptr] in self.token_tf_idf.keys():
                            #Gets old doc_id and its tf_idf score and updates it with a new doc_id and its tf_idf score
                            old_data = self.token_tf_idf[self.tokens_list[ptr]]
                            old_data.update({doc_id: tf_idf_score})
                            # updates the tokens doc_ids and all of its tf_idf scores
                            self.token_tf_idf.update({self.tokens_list[ptr]: old_data})
                        else:
                            # Adds the first doc_id and its score to the token 
                            self.token_tf_idf.update({self.tokens_list[ptr]: {doc_id: tf_idf_score}})

                    # move to the next token
                    ptr += 1
                    if ptr >= len(self.tokens_list): break
                    file.seek(self.table_of_contents[self.tokens_list[ptr][0]])

                # if the first letter of the token comes before the first letter of the current line
                elif self.tokens_list[ptr][0] < line[0]:
                    ptr += 1
                    if ptr >= len(self.tokens_list): break

                line = file.readline()
    
    # this function will parse the line of the file to get the 
    # doc ids from the line
    def parse_line(self, line:string):
        tokens = line.split()
        doc_id = []
        token_occurrences = []
        # Gets the numbers of the ids that relate to the tokem 
        
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

    def find_intersection(self):
        for token in self.tokens_list:
            if token not in self.token_documents.keys():
                return [] 

        intersections = []

        # create a parallel list of pointers
        pointers = []
        lengths = []
        for key in self.tokens_list:
            pointers.append(0)
            lengths.append(len(self.token_documents[key]))

        # find the smallest document
        smallest = 0
        for i, keyword in enumerate(self.tokens_list):
            if len(self.token_documents[keyword]) < len(self.token_documents[self.tokens_list[smallest]]):
                smallest = i

        # while we still have documents in the shortest list of document ids
        while (pointers[smallest] < len(self.token_documents[self.tokens_list[smallest]])):
            # assume the document id was found
            document_id_shared = True

            # search the other token lists
            for i, token in enumerate(self.tokens_list):
                # only check the tokens that aren't the smallest
                if token != self.tokens_list[smallest]:
                    # search each token's list for the same document id
                    
                    # while (current pointer hasn't reached the end of its respective list AND the current value hasn't gone past the value that we're looking for from the shortest list)
                    while (pointers[i] < len(self.token_documents[token]) and int(self.token_documents[token][pointers[i]]) < int(self.token_documents[self.tokens_list[smallest]][pointers[smallest]])):
                        pointers[i] += 1
                    
                    # if it made it here, it means that this token must be caught up. if it isn't equal, then it must not have found the 
                    # document id, so this current document id must not be shared amongst all the tokens
                    if (pointers[i] >= len(self.token_documents[token]) or self.token_documents[token][pointers[i]] != self.token_documents[self.tokens_list[smallest]][pointers[smallest]]):
                        document_id_shared = False
                        break
            
            # if they all share the current document, add it to the list
            if document_id_shared:
                intersections.append(self.token_documents[self.tokens_list[smallest]][pointers[smallest]])

            # increment the shortest pointer
            pointers[smallest] += 1
        
        return intersections

    def rank_urls(self, intersections: list) -> list:
        pairs = []

        # for each intersection (document_id)
        for intersection in intersections:
            sum = 0
            # get the sum of frequencies for each word in the current token list
            for token in self.tokens_list:
                index = self.token_documents[token].index(intersection)
                sum += int(self.token_frequencies[token][index])

            # add the current intersection and its sum into a list of pairs
            pairs.append((intersection, sum))

        # sort the list of pairs by their sums
        pairs = sorted(pairs, key = lambda x: x[1], reverse=True)

        # return a list of just the intersections
        return_list = []
        for pair in pairs:
            return_list.append(pair[0])

        return return_list


    def get_doc_url(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            while True:
                line = file.readline()
                # if reached end of text file
                if not line:
                    break
                k,v = line.split(':', 1)
                v = v.replace('\n','')
                self.doc_id.update({k: v})
            return self.doc_id

    # This function will get the highest from the intersections and return them sorted. 
    # we calculate the highest td-idf score between the tokens and the intersected doc_ids
    # we will add up the scores for the the different tokens and td_idf score and get the highest from that
    # for example we have machine learning: machine: (1,.5) (3, .7) learning: (1, .2) (3 , .1)
    # our final score for these intersections doc_id will be (1, .7) and (3, .8)
    def highest_tf_idf_scores(self):
        #calls find_intersections to get a list of all the intersections 
        intersections = self.find_intersection()
        highest_if = {}
        #creates a map to have the intersections and a default tf_idf score of 0
        for intersect in intersections:
            highest_if.update({intersect: 0})

        #loops through each token in the query to get add up its scores
        for token in self.tokens_list:
            #loops through the doc_ids that are intersected 
            for intersect in intersections:
                value = self.token_tf_idf[token][intersect]
                old_value = highest_if[intersect]
                #adds up the intersected td_idf score
                highest_if.update({intersect: value + old_value})
        #gets the highest if_idf score and sorts them
        highest_if_id = sorted(highest_if, key=highest_if.get)
        return highest_if_id
      
    def create_table_of_contents(self) -> None:
        headers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', \
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', \
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        with open('indexes/index.txt', 'r') as file:
            # Read in the file once and build a list of line offsets
            offset = 0
            ptr = 0
            for line in file:
                # if the first line with the current char that the ptr is pointing
                # to, add the current offset to the map
                if line[0] == headers[ptr]:
                    self.table_of_contents[headers[ptr]] = offset
                    ptr += 1
                    if ptr >= len(headers): break

                offset += len(line)