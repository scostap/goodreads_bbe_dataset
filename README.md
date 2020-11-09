# Goodreads Best Books Ever dataset

This Python project was created to retrieve data from the Best Books Ever list on Goodreads.com using Python + Selenium as part of a academic work. 

The dataset folder contains the BBE_dataset published under CC BY-NC 4.0 and can be referenced as follows:

Lorena Casanova Lozano, & Sergio Costa Planells. (2020). Best Books Ever Dataset (Version 1.0.0) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4265096

**Group members:**
* Lorena Casanova Lozano
* Sergio Costa Planells

## Introduction

The dataset has been collected in the framework of Practice 1 of subject Tipology and Data Life Cycle of the Master's Degree in Data Science of the Universitat Oberta de Catalunya (UOC). 

This repository includes the developed tools needed to extract book information from any list on GoodReads.com. Documentation and usage examples are provided as well. 

## Contents
*/src/* --> Directory containing the source code used to generate the BBE dataset.

*/src/goodreadsscrapper.py* --> Python module containing the GoodReadsScrapper class to extract information from the Goodreads page via web scrapping with Selenium. 

*/src/main.py* --> Main program wich uses GoodReadsScraper to extract information from the Best_Books_Ever list on GoodReads.com

*/Docs_&_Examples/Read_BBE_dataset.ipynb* --> Jupyter Notebook containing an example code to read the generated dataset.

*/Docs_&_Examples/Documentation_GoodReadsScraper.pdf* --> Documentation on GoodReadsScraper usage.

*/Docs_&_Examples/silly_usage_example/* --> Usage example of GoodReadsScrapper applied to an small list. Shows complete functionality in ~2 minutes run.

*/Best_Books_Ever_dataset/books_1.Best_Books_Ever.csv* --> CSV containint the BBE dataset.

## Dataset Information

| Attributes  | Definition | Completeness |
| ------------- | ------------- | ------------- | 
| bookId  | Book Identifier as in goodreads.com  | 100 |
| title  | Book title | 100 |
| series | Series Name | 45 |
| author | Book's Author | 100 |
| rating | Global goodreads rating | 100 |
| description | Book's description | 97 |
| language | Book's language | 93 |
| isbn | Book's ISBN | 92 |
| genres | Book's genres | 91 |
| characters | Main characters | 26 |
| bookFormat | Type of binding | 97 |
| edition | Type of edition (ex. Anniversary Edition) | 9 |
| pages | Number of pages | 96 |
| publisher | Editorial | 93 |
| publishDate | publication date | 98 |
| firstPublishDate | Publication date of first edition | 59 |
| awards | List of awards | 20 |
| numRatings | Number of total ratings | 100 |
| ratingsByStars | Number of ratings by stars | 97 |
| likedPercent | Derived field, percent of ratings over 2 starts (as in GoodReads) | 99 |
| setting | Story setting | 22 |
| coverImg | URL to cover image | 99 |
| bbeScore | Score in Best Books Ever list | 100 |
| bbeVotes | Number of votes in Best Books Ever list | 100 |
| price | Book's price (extracted from Iberlibro) | 73 |

Book cover images are not provided within the dataset, but the dataset contains the URL to each book's cover image and the GoodReadsScraper can be used to download them. Usage is documented and a simple example is provided (see /Docs_&_Examples/silly_usage_example/).

More information on the dataset can be obtained at http://doi.org/10.5281/zenodo.4265096
