
class Index():
    def __init__(self):
        self.doc_id = {}            # associate each url with an id, e.g. {"https://ics.uci.edu": 1, "https://reddit.com": 2}
        self.current_id = 1         # increment each time after an id is associated with a document
        self.token_id = {}          # associate each token with the document where it appears, e.g. {"anteater": [1], "zot": [1,4]}
                                    # this is a list of tuples

    def extract_content(self):
        # read from a json file
        # extract content from json files
        # return a list of words including stop words
        return 0

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
       

    def tokenize(self):
        # normalize the words to token, e.g. U.S.A to USA, etc.
        # I think we are allowed to use a library
        # return a list of tokens
        return 0

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