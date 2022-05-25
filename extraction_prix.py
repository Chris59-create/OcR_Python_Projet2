import requests
from bs4 import BeautifulSoup
import re
import csv

# boucler dans toutes les pages d'une catégorie
urlBooksList =[]
page_category_url =('http://books.toscrape.com/catalogue/category/books'
                    '/mystery_3/index.html')
page_category = requests.get(page_category_url)
soup_category = BeautifulSoup(page_category.content, 'html.parser')
for href in soup_category.find_all('a', title=True):
    urlBook = "http://books.toscrape.com/catalogue" + href['href'][8:]
    urlBooksList.append(urlBook)
print(urlBooksList)



#image_url = "htpp://books.toscrape.com" + img_tag['src'][5:]
# extract url de chaque page produit
'''
# Extraction à partir page produit

# Récupération code source de la page
product_page_url = ("http://books.toscrape.com/catalogue/a-light-in-the"
                    "-attic_1000/index.html")
page = requests.get(product_page_url)
soup = BeautifulSoup(page.content, 'html.parser')

# Extraction des données dispersées et ajout dans dictionnaire
extracts = {}

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

# Extraction données du tableau html et ajout dans dictionnaire
trs = soup.find_all("tr")
for tr in trs:
    th = tr.find("th")
    td = tr.find("td")
    extracts[th.string] = td.string
#print(extracts)

# Ecriture des données dans fichier csv
en_tete = ["universal_ product_code (upc)", "title", "price_including_tax",
    "price_excluding_tax", "number_available", "product_description",
    "category", "review_rating", "image_url"
    ]
source_en_tete = ["UPC", "title", "Price (incl. tax)", "Price (excl. tax)",
    "Availability", "product_description", "category", "star-rating",
    "image_url"
    ]
source_data = []
with open('bookstoscrape_data.csv', 'w') as file_csv:
    writer = csv.writer(file_csv, delimiter=',')
    writer.writerow(en_tete)

    for destination_key, source_key in zip(en_tete, source_en_tete):
        item = extracts[source_key]
        source_data.append(item)

    writer.writerow(source_data)
'''