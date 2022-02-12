from lib2to3.pgen2 import token
from Indexer import Index

def run():
    test_json_file = "8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json"

    # a loop going over all the files in DEV need to happen here
    # this is just an example
    index = Index()
    
    while (True):     
        token_list = index.extract_content(test_json_file)
        stem_list = index.stem(token_list)
        index.create_pair_file(token_list)
        print(index.token_id)
        # once in a while, clear the memory and output those to a text file
        

        print(stem_list)
        break




if __name__ == '__main__':
    run()