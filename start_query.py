from Query import Query
import time

def main():
    test = Query()
    test.get_doc_url('documentIDs.txt')
    # populate the offset map
    # i.e., index the index
    test.create_table_of_contents()

    while True:
        # start the timer
        t = time.process_time()

        # get user input, and check if we need to terminate the program
        user_input = test.get_input()
        if user_input == '-1': break

        # retrieve the relevant documents for the current qu5ery
        test.retrieve_relevant_document('indexes/index.txt')

        # find all of the results, sorted by rank
        sorted_intersections = test.highest_tf_idf_scores()

        # print the results in order
        for i in range(5):
            # ensure we don't go out of bounds for results
            if i >= len(sorted_intersections): break
            print(test.doc_id[sorted_intersections[i]])

        # calculate the total time for the query, and print in ms
        elapsed_time = round((time.process_time() - t) * 1000)
        print('elapsed time:', elapsed_time, 'milliseconds\n')

if __name__ == '__main__': main()