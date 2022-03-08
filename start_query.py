from Query import Query
import time
from tkinter import *

def run_query(window: Tk, test: Query, data: str):
    # start the timer
    t = time.process_time()

    # get user input, and check if we need to terminate the program
    user_input = test.get_input(data)

    # retrieve the relevant documents for the current qu5ery
    test.retrieve_relevant_document('indexes/index.txt')

    # find all of the results, sorted by rank
    sorted_intersections = test.highest_tf_idf_scores()

    # top 5 results
    for i in range(5):
        # destroy previous label
        if test.links[i] != None: test.links[i].destroy()

        # create label
        test.links[i] = Label(window, font=('Arial',12), fg='blue')

        # ensure we don't go out of bounds for results
        if i >= len(sorted_intersections): break

        # print result in console
        print(test.doc_id[sorted_intersections[i]])

        # print results in GUI
        test.links[i].grid(row=i+3,column=1,columnspan=5,sticky=W)
        test.links[i].config(text='')
        test.links[i].config(text=str(test.doc_id[sorted_intersections[i]]))

    # Abomination, DO NOT REVIVE
    # l = len(sorted_intersections)
    # if l == 1:
    #     test.links[0].bind('<Button-1>', lambda e: open_url(sites[0]))
    # elif l == 2: 
    #     test.links[0].bind('<Button-1>', lambda e: open_url(sites[0]))
    #     test.links[1].bind('<Button-1>', lambda e: open_url(sites[1]))
    # elif l == 3:
    #     test.links[0].bind('<Button-1>', lambda e: open_url(sites[0]))
    #     test.links[1].bind('<Button-1>', lambda e: open_url(sites[1]))
    #     test.links[2].bind('<Button-1>', lambda e: open_url(sites[2]))
    # elif l == 4:
    #     test.links[0].bind('<Button-1>', lambda e: open_url(sites[0]))
    #     test.links[1].bind('<Button-1>', lambda e: open_url(sites[1]))
    #     test.links[2].bind('<Button-1>', lambda e: open_url(sites[2]))
    #     test.links[3].bind('<Button-1>', lambda e: open_url(sites[3]))
    # elif l == 5:
    #     test.links[0].bind('<Button-1>', lambda e: open_url(sites[0]))
    #     test.links[1].bind('<Button-1>', lambda e: open_url(sites[1]))
    #     test.links[2].bind('<Button-1>', lambda e: open_url(sites[2]))
    #     test.links[3].bind('<Button-1>', lambda e: open_url(sites[3]))
    #     test.links[4].bind('<Button-1>', lambda e: open_url(sites[4]))

    # calculate the total time for the query, and print in ms
    elapsed_time = round((time.process_time() - t) * 1000)
    print('elapsed time:', elapsed_time, 'milliseconds\n')

    elapsed_label = Label(window, font=('Arial',12), fg='red')
    elapsed_label.grid(row = 9, column=1, sticky=W)
    elapsed_label.config(text='Elapsed time: ' + str(elapsed_time) + 'ms')

def main():
    test = Query()
    test.get_doc_url('documentIDs.txt')
    # populate the offset map
    # i.e., index the index
    test.create_table_of_contents()

    # GUI #
    # main window
    window = Tk()
    window.title('CS-121 Search Engine')
    window.geometry('1000x500')

    # search label
    label1 = Label(window, text='Enter your search: ', fg='black')
    label1.grid(row=0, column=0, padx=5, pady=10)

    # input data
    data = StringVar()

    # search textbox
    textbox1 = Entry(window, textvariable=data, font=('Arial',14))
    textbox1.grid(row=0, column=1,sticky=W)
    textbox1.focus()

    # search button
    button1 = Button(window,command=lambda: run_query(window,test,data.get()), text='Search', font=('Arial',14))
    button1.grid(row=1,column=1,sticky=W)

    # bind Enter key to Search
    window.bind('<Return>', lambda eff: run_query(window, test,data.get()))# lambda: run_query(window,test,data.get()))

    # loop
    window.mainloop()

if __name__ == '__main__': main()