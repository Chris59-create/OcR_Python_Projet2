import requests
from bs4 import BeautifulSoup
import re
import os
import csv

print('\n', "Welcome! You begin to scrape http://books.toscrape.com/", '\n')

# horme url of the site to scrape
homeUrl = 'http://books.toscrape.com/'

# Create the directory csv-files in the current directory
# To store the csv files per category
dirCsv = 'csv_files'
if not os.path.exists(dirCsv):
    print("The directory 'csv_files' is created in the current directory. For "
          "each category of books, each data extracted per book is stored in "
          "a csv file named with the name of the category. These csv_files is "
          "located in the created directory.", '\n')
    os.mkdir(dirCsv)
else:
    print("The directory 'csv_files' already exists in the current directory",
          '\n')
# Create the directory books_img in the current directory
# To store the subdirectories per category for books img
dirImg = "img_directories"
if not os.path.exists(dirImg):
    print("The directory 'img_directories' is created in the current "
          "directory. In this just created directroy, each image of a book is "
          "stored in a named nameCategory_img subdirectory. The image file "
          "is named with the UPC of the relative book", '\n')
    os.mkdir(dirImg)
else:
    print("The directory 'img_directories' already exists in the current "
          "directory", '\n')

# Library of functions


# Load the source code of the page
def productPageContent(url):
    product_page_url = url
    page = requests.get(product_page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


# List of all categories's urls of the home page
def urlCategoriesExtract(soup):
    urlCategoriesList = []
    for href in soup.find_all('a', href=re.compile("/category/")):
        urlCategory = "http://books.toscrape.com/" + href['href']
        urlCategoriesList.append(urlCategory)
    del urlCategoriesList[0]
    print(f"{len(urlCategoriesList)} urls of categories are extracted", '\n')
    return urlCategoriesList

# List names of categories extracted from categories urls
def namesCategories(urlCategoriesList):
    nameCategoryList = []
    for item in urlCategoriesList:
        urlCategorySplit = item.split('/')
        nameCategory = urlCategorySplit[-2].split("_")[-2]
        nameCategoryList.append(nameCategory)
    # Preparation of print of names of category like table
    print("-" * 72, '\n', "Names of the categories:", '\n')
    board = []
    for name in nameCategoryList:
        board.append(name)
        l = len(board)
        if l % 5 == 0:
            print(board[l - 5:l], '\n')
    return nameCategoryList


# List of all book's urls of the category page
def urlBooksExtract(category_url):
    urlBooksList = []
    page_category = requests.get(category_url)
    soup_category = BeautifulSoup(page_category.content, 'html.parser')
    for href in soup_category.find_all('a', title=True):
        urlBook = "http://books.toscrape.com/catalogue" + href['href'][8:]
        urlBooksList.append(urlBook)
    return urlBooksList


# Create dictionary of book data
def dataDict(soup, urlbook):
    # Initialization data dictionary
    extracts = {}

    # Extract of data

    extracts["product_page_url"] = urlbook

    th = soup.find('th', text="UPC")
    extracts["universal_ product_code (upc)"] = th.findNext('td').text

    title = soup.find("li", class_="active")
    extracts["title"] = title.string

    th = soup.find('th', text="Price (incl. tax)")
    extracts["price_including_tax"] = float(th.findNext('td').text.replace(
        "£", ""))

    th = soup.find('th', text="Price (excl. tax)")
    extracts["price_excluding_tax"] = float(th.findNext('td').text.replace(
        "£", ""))

    th = soup.find('th', text="Availability")
    td = th.findNext('td').text
    extracts["number_available"] = ([int(s) for s
                                     in td.replace("(", "").split()
                                     if s.isdigit()][0])

    paragraphe = soup.findAll('p', {})
    extracts["product_description"] = paragraphe[3].string

    category = soup.find("a", href=re.compile("/books/"))
    extracts["category"] = category.string

    review_rating = soup.find(class_=re.compile("star-rating"))
    extracts[review_rating['class'][0]] = review_rating['class'][1]

    image_tag = soup.find('div', class_= "item active")
    img_tag = image_tag.img
    image_url = "http://books.toscrape.com" + img_tag['src'][5:]
    extracts["image_url"] = image_url

    return extracts


# Writing of the book data in the csv file
def csvEcrit(extracts):
    source_data = []
    for key in extracts:
        item = extracts[key]
        source_data.append(item)
    writer = csv.writer(file_csv, delimiter=',')
    writer.writerow(source_data)

# Main code

# Create the list of categories and categories names of the site
soup = productPageContent(homeUrl)
urlCategoriesList = urlCategoriesExtract(soup)
namesCategoriesList= namesCategories(urlCategoriesList)

# Treatment of each category
for urlCategory, nameCategory in zip(urlCategoriesList, namesCategoriesList):
    # Extract root of the category url
    urlRoot = urlCategory[:-10]
    # Extract the code source of the first of category
    soupCategory = productPageContent(urlCategory)
    # list urls of products pages from the first page
    # of the category
    urlBooksList = urlBooksExtract(urlCategory)
    # If next page add urls of products pages of nexct pages
    while soupCategory.find('li', class_="next"):
        nextPage = soupCategory.find('a', text="next")
        nextPageUrl = urlRoot + nextPage['href']
        soupCategory = productPageContent(nextPageUrl)
        urlBooksList += urlBooksExtract(nextPageUrl)
    print("-"*72, '\n')
    print(f"{len(urlBooksList)} url(s) of book(s) of the categorie"
                f" {nameCategory} are extracted", '\n')

    # Create the csv file of the category with first row en_tete"
    # in the folder csv_files
    nameCsv = "csv_files/" + nameCategory + "_data.csv"
    en_tete = ["product_page_url", "universal_ product_code (upc)", "title",
               "price_including_tax",
               "price_excluding_tax", "number_available",
               "product_description",
               "category", "review_rating", "image_url"
               ]
    with open(nameCsv, 'w') as file_csv:
        writer = csv.writer(file_csv, delimiter=',')
        writer.writerow(en_tete)
        print(f"The file '{nameCsv}' is created", '\n')

        #Extract books data of the category
        imgNumber = 0
        for urlBook in urlBooksList:
            soup = productPageContent(urlBook)
            extracts = dataDict(soup, urlBook)
            # Write the books data in a csv file for the category
            csvEcrit(extracts)
            # if not exist create directory for download images of category
            pathCategoryImg = dirImg + "/" + nameCategory + "_img"
            if not os.path.exists(pathCategoryImg):
                os.mkdir(pathCategoryImg)
                print(f"The subdirectory '{pathCategoryImg}' is "
                            f"created")
            # Download the image of the current book in the directory
            urlImg = extracts["image_url"]
            fileTypImg = urlImg.split(".")[-1]
            # Image of the book named wiht book UPC
            fileName = (pathCategoryImg + "/"
                        + extracts["universal_ product_code (upc)"]
                        + "." + fileTypImg)
            r = requests.get(urlImg)
            with open(fileName, 'wb') as file:
                file.write(r.content)
                imgNumber += 1
        print(f"{imgNumber} images are downloaded for the "
                    f"category '{nameCategory}'.", '\n')

print(f"The scrapping of the url '{homeUrl}' is ended", '\n', "You can find "
        "the extracted data in the subdiretory 'csv_files' in the current "
        "directory and the images of the books in the subdirectory "
        "'img_directories'.")