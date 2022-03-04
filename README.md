# CS-121 Search-Engine

## Summary
This Search engine does the following things in order:
<ul>
    <li>It takes a corpus of json files and extract the html content from them.
    <li>The html contents are parsed to create tokens which are then stemmed.
    <li>A merged index file is created on the disk with the tokens as keys and postings as values. A posting is in the tuple format (documentID, frequency) where documentID is the id of the document where the token appeared and the token frequency is the number of times the token appears.
    <li>A document id file is also created to help return the urls of the search results.
    <li>
    <li>
</ul>

## Note
<br></br>
To test on all documents, extract the `developer.zip` and have the content `DEV` folder in the root. The folder is not uploaded here due to size.
<br></br>
This `DEV` folder is included in the `.gitignore` and therefore will not be included when pushing.


## Dependencies
<ol>
    <li>NLTK - installed via ```pip install --user -U nltk```
        <ul>
            <li>NLTK is short for Natural Language Tool Kits which needss to be installed to be able to use its PorterStemmer function.
        </ul>
    <li>Beautiful Soup - installed via ```pip install --user -U beautifulsoup4
        <ul>
            <li>Beautiful Soup is used for parsing HTML content extrated from the json files.
        </ul>
</ol>

## How to run
