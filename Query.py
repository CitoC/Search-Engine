import string
from Indexer import Index
from nltk.stem import PorterStemmer
class Query():

    def __init__(self):
        self.tokens_list = []
        self.token_documents = {}
        

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
        print(self.tokens_list)
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
                        doc_ids = self.parse_line(line)
                        self.token_documents.update({token: doc_ids})
                        break
    
    
    #this function will parse the line of the file to get the 
    #doc ids from the line
    def parse_line(self, line:string):
        tokens = line.split()
        doc_id = []
        #Gets the numbers of the ids that relate to the tokem 
        for token in tokens:
            if token.isdigit():
                doc_id.append(token)
        return doc_id

    #test function
    def print_id(self):
        print(self.token_documents)
        

        