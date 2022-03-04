from Query import Query
import time

def main():
    test = Query()
    while True:
        test.get_doc_url('documentIDs.txt')
        
        t = time.process_time()

        user_input = test.get_input()
        if user_input == '-1': break

        test.retrieve_relevant_document('indexes/index.txt')

        sorted_intersections = test.highest_tf_idf_scores()

        for i in range(5):
            print(test.doc_id[sorted_intersections[i]])

        elapsed_time = round((time.process_time() - t) * 1000)
        print('elapsed time:', elapsed_time, 'milliseconds\n')
        

        del test
        test = Query()

if __name__ == '__main__': main()