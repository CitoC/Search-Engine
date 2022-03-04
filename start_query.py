from Query import Query
import time

def main():
    test = Query()
    test.get_doc_url('documentsIDs.txt')
    
    while True:
        
        # get the start time (to determine running time of searches)
        t = time.process_time()

        # prompt user to enter a search term
        user_input = test.get_input()
        if user_input == '-1': break

        # read relevant data from index file from disk into memory
        test.retrieve_relevant_document('indexes/index.txt')

        # calculate document rankings
        sorted_intersections = test.highest_tf_idf_scores()

        # get top 5 search results
        for i in range(5):
            print(test.doc_id[sorted_intersections[i]])

        # calculate elasped time for search
        elapsed_time = round((time.process_time() - t) * 1000)
        print('elapsed time:', elapsed_time, 'milliseconds\n')
        

        del test
        test = Query()

if __name__ == '__main__': main()
