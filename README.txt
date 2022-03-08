Leo Baleon - 81387788
Joshua Montellano - 80502029
Arkar Chan - 15146128

# There is better formatted documentation on Github #
https://github.com/CitoC/Search-Engine/blob/main/README.md


Summary
This Search engine does the following things in order:

It takes a corpus of json files and extract the html content from them.
The html contents are parsed to create tokens which are then stemmed.
A merged index file is created on the disk with the tokens as keys and postings as values. A posting is in the tuple format (documentID, frequency) where documentID is the id of the document where the token appeared and the token frequency is the number of times the token appears.
A document id file is also created to help return the urls of the search results.
For searching, the user will be prompted to enter a search term.
The search will then return a top 5 urls that matches the search terms.
Searches will continue until ther user enter -1.

Dependencies
NLTK - installed via pip install --user -U nltk
NLTK is short for Natural Language Tool Kits which needss to be installed to be able to use its PorterStemmer function.
Beautiful Soup - installed via pip install --user -U beautifulsoup4
Beautiful Soup is used for parsing HTML content extrated from the json files.

How to run
Place all json files that you want to include in the corpus in a folder called DEV.
Run create_index.py to create the index file. The index.txt will appear in the current directory.
Run idURL.py to create the document ids file. The documentIDs.txt will appear in the current directory.
Run start_query.py to start the search. The user will be prompt to enter a search term until -1 is entered.
