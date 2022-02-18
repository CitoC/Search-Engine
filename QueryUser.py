import string
from Indexer import Index
class QueryUser():

    def __init__(self, index:Index):
        self.index = index
        pass

    #This function will read in the input and tokenize the input for retrieval
    #of the document in the index
    #Only need to test the querys (cristina lopes, machine learning, ACM, master of software engineering)
    def get_input(self, input:string):
        pass

    #this function will go through the index and retrieve the relevant 
    #documents releated to the query
    #the majority of milestone 2 will probably be involved here(might need more functions to help the processing)
    # returns a list of the relevent documents to compare
    def retrieve_relevant_document(self):
        pass