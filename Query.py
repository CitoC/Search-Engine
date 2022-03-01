import string
from Indexer import Index
from nltk.stem import PorterStemmer
class Query():

    def __init__(self):
        self.tokens_list = []
        self.token_documents = {}
        self.token_frequencies = {}

    #This function will read in the input and tokenize the input for retrieval
    #of the document in the index
    #Only need to test the querys (cristina lopes, machine learning, ACM, master of software engineering)
    def get_input(self):
        #will split by white space to see get the tokens of the query that must be processed
        #should be simple for the queries for milestone 2 will need changes later on
        query = input("Search: ")
        tokens =  query.split()
        ps = PorterStemmer()

        for token in tokens:
            self.tokens_list.append(ps.stem(token))
        # print(self.tokens_list)
        return query
        #print(self.tokens_list)

    #this function will go through the index and retrieve the relevant 
    #documents releated to the query
    #Might need need to call more than once with multiple files 
    def retrieve_relevant_document(self, file_name):
        with open(file_name, 'r') as file:
            #Goes through the file line by line 
            for line in file:
                #checks to see if the token is in that line 
                for token in self.tokens_list:
                    #If the token is in the line find its elements
                    #print(token)
                    #if token in line:
                    if token  + '\t' == line[0:len(token) + 1]:
                        doc_ids, token_occurrences = self.parse_line(line)
                        self.token_documents.update({token: doc_ids})
                        self.token_frequencies.update({token: token_occurrences})
                        break

    # def parse_line(self, line:string):
    #     tokens = line.split()
    #     doc_id = []
    #     #Gets the numbers of the ids that relate to the tokem 
    #     for token in tokens:
    #         if token.isdigit():
    #             doc_id.append(token)
    #     return doc_id
    
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

    def find_intersection(self):
        for token in self.tokens_list:
            if token not in self.token_documents.keys():
                return [] 

        intersections = []
        # map is called self.token_documents

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

                # move over all of our pointers to their respective next document ids
                for i, pointer in enumerate(pointers):
                    pointers[i] += 1
            else:
                # increment the shortest pointer
                pointers[smallest] += 1
        
        return intersections

    #test function
    def print_id(self):
        print(self.token_documents)

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