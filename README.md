# Goodreads Best Books Ever dataset

This is a Python project to retrieve data from list of Best Books Ever from page Goodreads using Selenium. 

**Group members:**
* Lorena Casanova Lozano
* Sergio Costa Planells

## Introduction

The obtained dataset has been collected in the framework of Practice 1 of subject Tipology and Data Life Cycle of the Master's Degree in Data Science of the Universitat Oberta de Catalunya (UOC). 

In this repository there are the .py files that allow to extract the information like title, author, isbn, score, etc. from the books published in the Best Books Ever list of the Goodreads page. It also contains the functions to extract the price of the book from other web pages through its isbn or title and author. 

## Code

*/src/goodreadsscrapper.py* --> Python code with the GoodReadsScrapper class to extract information from the Goodreads page via web scrapping with Selenium. Use the URL of the page of each of the books you want to extract the information and iterate through each of its elements until you get a list with all the attributes.

*/src/main.py* --> Run goodreadsscrapper.py functions.

*/Docs_&_Examples/Read_BBE_dataset.ipynb* --> Jupyter Notebook script to read the generated dataset of Best Books Ever list from Goodreads

*/Docs_&_Examples/silly_usage_example/main.py* --> An example to take the first 9 books of Best Books Ever list from Goodreads



## Dataset Information

| Attributes  | Definition |
| ------------- | ------------- |
| bookId  | Book Identifier in goodreads.com  |
| title  | Book title |
| series | Saga Name |
| author | Book's Author |
| rating | Global Score in goodreads |
| description | Book's description |
| language | Book's language |
| isbn | Book's ISBN |
| genres | Book's genres |
| characters | Main protagonists' name |
| bookFormat | Type of binding |
| edition | Type of edition (ex. Anniversary Edition) |
| pages | Number of pages |
| publisher | Editorial |
| publishDate | publication date |
| firstPublishDate | First publication date |
| awards | List of awards |
| numRatings | Number of total valuations |
| ratingsByStars | Number of valuations by stars |
| likedPercent | Percent of readers who liked book |
| setting | Location of history |
| coverImg | Cover image with png format |
| bbeScore | Score in Best Books Ever list |    
| bbeVotes | Number of votes in Best Books Ever list |
| price | Book's price (extracted from Iberlibro) |
