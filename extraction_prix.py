import requests
from bs4 import BeautifulSoup
import re
import csv


# Load the source code of the page
def productPageContent(url):
    product_page_url = url
    page = requests.get(product_page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print("Soup : ", soup)
    return soup


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
def dataDict(soup):
    # Initialisation du dictionnaire de données
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
    print("extracts : ", extracts)

    return extracts


# Writing of the book data in the csv file
def csvEcrit(extracts):

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


# Creation of the csv file with first row en_tete"
en_tete = ["universal_ product_code (upc)", "title", "price_including_tax",
        "price_excluding_tax", "number_available", "product_description",
        "category", "review_rating", "image_url"
        ]
with open('bookstoscrape_data.csv', 'w') as file_csv:
    writer = csv.writer(file_csv, delimiter=',')
    writer.writerow(en_tete)

# Extract of the code source of the page index of category
urlCategory = ('http://books.toscrape.com/catalogue/category'
    '/books/mystery_3/index.html')
# Category url split in variables
urlSplit = urlCategory.split("/")
urlEnd = urlSplit[-1]
nameCategory = urlSplit[-2]
urlRoot = ""
for part in urlSplit[:-1]:
    urlRoot += part + "/"
# Extract of the code source of the page Category
soupCategory = productPageContent(urlCategory)
# Extract of the number of pages of the category
pagesNumberExtract = soupCategory.find('li', class_="current")
pagesNumberText = pagesNumberExtract.text.split()
pagesNumber = int(pagesNumberText[-1])
# list urls of products pages from the first page of category
# of the category
urlBooksList = urlBooksExtract(urlCategory)
# Loop for data extract for all books on all pages of category
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
    i += 1