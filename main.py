


from Indexer import Index

def run():
    # a loop going over all the files in DEV need to happen here
    # this is just an example
    while (True):       
        Index.extract_content()
        Index.tokenize()
        Index.stem()

        # once in a while, clear the memory and output those to a text file





if __name__ == '__main__':
    run()