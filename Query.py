import string
from Indexer import Index
from nltk.stem import PorterStemmer
class Query():

    def __init__(self, index:Index):
        self.index = index
        self.tokens_list = []
        

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
        #print(self.tokens_list)

    #this function will go through the index and retrieve the relevant 
    #documents releated to the query
    #the majority of milestone 2 will probably be involved here(might need more functions to help the processing)
    # returns a list of the relevent documents to compare
    def retrieve_relevant_document(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                for token in self.tokens_list:
                    if token in line:
                        pass
    
    #this function will parse the line of the file to get the 
    def parse_line(self):
        pass
        