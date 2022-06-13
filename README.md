# Scrape a books website to learn Python
## Overview
This python program is written as **study case** to be evaluated for validation of the project 2 of the **OpenClassrooms Python training courses**. The purpose is to ***scrape the website of [Books to scrape](http://books.toscrape.com/)***, an online books reseller. The program doesn't watch the website in real time, but on demand will extract some data, especially the prices, of the books sold by the website.

## Configuration
- macOS 12.4 21F79
- Python 3.10.4
- Packages environnement, see [requirements.txt](/requirements.txt)

## Features
1. Create a subdirectory `csv_files` in the current directory to store the csv files wich will contains the data of the books.
2. Create subdirectory `ìmg_subsidories` in the current directory to store the images of the books downloaded from the website.
3. Extracts all the urls of the categories of books.
4. Extracts all the categories names.
5. Per category: extracts all books urls.
6. Per book of the category:
    1. Extracts the following data :
      - Product_page_url
      - Universal_ product_code (upc)
      - Title
      - Price_including_tax
      - Price_excluding_tax
      - Number_available
      - Product_description
      - Category
      - Review_rating
      - Image_url
    2. Writes the data in a csv file named `nameCategory_data.csv`. The csv file is stored in the subdirectory `csv_files`.
    3. Downloads the image of the book as `Universal_product_code.(filetyp of the image source)` in a subdirectory named `nameCategory_img`.
               
## How to use the program
- [] Clone [the github repository](https://github.com/Chris59-create/ocr_python_projet2.git) locally
- [] Install the packages according the configuration file `$ pip install -r requirements.txt`.
– []Run the program `$ python extraction_prix.py`.

During the process, dynamic messages will show you the step one of the scrapping

## Credits
Author: Chris59create (Chris59-create)

**Beware this a a coding for a training evaluation. The use of this code (Cloning, global or incomplete copy or re use of it) is forbidden.**
