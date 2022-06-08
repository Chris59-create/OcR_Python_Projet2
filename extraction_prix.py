import requests
from bs4 import BeautifulSoup
import re
import csv

homeUrl = 'http://books.toscrape.com/'


# Load the source code of the page
def productPageContent(url):
    print('/n', "début productPageContent(url)", '/n',)# for test
    product_page_url = url
    page = requests.get(product_page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print("Soup : ", soup)
    print('/n', "end productPageContent(url)", '/n',)# for test
    return soup


# List of all categories's urls of the home page
def urlCategoriesExtract(soup):
    print('/n', "début urlCategoriesExtract(soup)", '/n')# for test
    urlCategoriesList = []
    for href in soup.find_all('a', href=re.compile("/category/")):
        urlCategory = "http://books.toscrape.com/" + href['href']
        urlCategoriesList.append(urlCategory)
    print(urlCategoriesList)# for test
    print('/n', "fin urlCategoriesExtract(soup)", '/n')# for test
    return urlCategoriesList

# List names of categories extracted from categories urls
def namesCategories(urlCategoriesList):
    print('/n', "début namesCategories", '/n')# for test
    nameCategoryList = []
    for item in urlCategoriesList[1:]:
        urlCategorySplit = item.split('/')
        nameCategory = urlCategorySplit[-2].split("_")[-2]
        nameCategoryList.append(nameCategory)
    print('/n', "fin namesCategories", '/n')# for test
    return nameCategoryList


# List of all book's urls of the category page
def urlBooksExtract(category_url):
    print('/n', "début urlBooksExtract", '/n')# for test
    urlBooksList = []
    page_category = requests.get(category_url)
    soup_category = BeautifulSoup(page_category.content, 'html.parser')
    for href in soup_category.find_all('a', title=True):
        urlBook = "http://books.toscrape.com/catalogue" + href['href'][8:]
        urlBooksList.append(urlBook)
    print('/n', "Fin urBooksExtract", '/n')# for test
    return urlBooksList


# Create dictionary of book data
def dataDict(soup):
    print('/n', "début dataDict(soup)", '/n')# for test
    # Initialization data dictionary
    extracts = {}

    # Extract disseminated data
    title = soup.find("li", class_="active")
    extracts["title"] = title.string

    paragraphe = soup.findAll('p', {})
    extracts["product_description"] = paragraphe[3].string

    category = soup.find("a", href=re.compile("/books/"))
    extracts["category"] = category.string

    review_rating = soup.find(class_=re.compile("star-rating"))
    extracts[review_rating['class'][0]] = review_rating['class'][1]

    image_tag = soup.find('div', class_= "item active")
    img_tag = image_tag.img
    image_url = "htpp://books.toscrape.com" + img_tag['src'][5:]
    extracts["image_url"] = image_url

    # Extract data of the html table and adding in dictionary
    trs = soup.find_all("tr")
    for tr in trs:
        th = tr.find("th")
        td = tr.find("td")
        extracts[th.string] = td.string
    print("extracts : ", extracts)# for test
    print('/n', "Fin dataDict")# for test
    return extracts


# Writing of the book data in the csv file
def csvEcrit(extracts):
    print('/n', "csvEcrit(extracts)", '/n')# for test
    source_en_tete = ["UPC", "title", "Price (incl. tax)", "Price (excl. tax)",
        "Availability", "product_description", "category", "star-rating",
        "image_url"
        ]
    source_data = []
    for destination_key, source_key in zip(en_tete, source_en_tete):
        item = extracts[source_key]
        source_data.append(item)

    with open('bookstoscrape_data.csv', 'a') as file_csv:
        writer = csv.writer(file_csv, delimiter=',')
        writer.writerow(source_data)

    print('/n', "Fin csvEcrit", '/n')# for test


# Create the list of categories of the site
soup = productPageContent(homeUrl)
urlCategoriesList = urlCategoriesExtract(soup)
namesCategoriesList= namesCategories(urlCategoriesList)
print("namesCategoriesList : ", namesCategoriesList)# for test

# Create the csv file with first row en_tete"
en_tete = ["universal_ product_code (upc)", "title", "price_including_tax",
        "price_excluding_tax", "number_available", "product_description",
        "category", "review_rating", "image_url"
        ]
with open('bookstoscrape_data.csv', 'w') as file_csv:
    writer = csv.writer(file_csv, delimiter=',')
    writer.writerow(en_tete)

#
for urlCategory in urlCategoriesList[1:]:
    # Extract root of the category url
    urlRoot = urlCategory[:-10]
    print(urlRoot)#for test
    # Extract of the code source of the page Category
    print("urlCategory", urlCategory)#for test
    soupCategory = productPageContent(urlCategory)
    # list urls of products pages from the first page of category
    # of the category
    urlBooksList = urlBooksExtract(urlCategory)

    while soupCategory.find('li', class_="next"):
        nextPage = soupCategory.find('a', text="next")
        nextPageUrl = urlRoot + nextPage['href']
        print(nextPageUrl)#for test
        soupCategory = productPageContent(nextPageUrl)
        urlBooksList += urlBooksExtract(nextPageUrl)

    print("list of book urls of category", urlBooksList)#for test
    #Extract of books data of the category
    extracts = dataDict(soupBook)



'''  # Loop for data extract for all books on all pages of category
# Extract of the number of pages of the category
pagesNumberExtract = soupCategory.find('li', class_="current")
pagesNumberText = pagesNumberExtract.text
pagesNumberTextSplit = pagesNumberText.split()
pagesNumber = int(pagesNumberTextSplit[-1])
i=0
while i in range(pagesNumber):
    print("Nombre de livres : ", len(urlBooksList))
    for urlBook in urlBooksList:
        url = urlBook
        print(url)
        soupBook = productPageContent(urlBook) 
        extracts = dataDict(soupBook)
        csvEcrit(extracts)
    # Url of the next page of the category
    nextPage = soupCategory.find('a', text="next")
    nextPageUrl = urlRoot + nextPage['href']
    print(nextPageUrl)
    urlBooksList = urlBooksExtract(nextPageUrl)
    print(i)
    i += 1'''