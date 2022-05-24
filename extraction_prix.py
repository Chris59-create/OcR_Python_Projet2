import requests
from bs4 import BeautifulSoup

recherche = ["universal_ product_code (upc)", "title", "price_including_tax",
    "price_excluding_tax", "number_available", "product_description",
    "category", "review_rating", "image_url"
    ]

print(recherche)

# Extraction à partir page produit
# Récupération code source de la page
product_page_url = ("http://books.toscrape.com/catalogue/a-light-in-the"
                    "-attic_1000/index.html")
page = requests.get(product_page_url)
soup = BeautifulSoup(page.content, 'html.parser')

# Extraction des données dispersées
extracts = {}
title = soup.find("li", class_="active")
extracts["title"] = title.string
p = soup.findAll('p', {})
extracts["product_description"] = p[3].string
category = soup.find_all('a',
                         href='http://books.toscrape.com/catalogue/category/books/poetry_23/index.html')
print("category", category)
#extraction données du tableau html
trs = soup.find_all("tr")
for tr in trs:
    th = tr.find("th")
    td = tr.find("td")
    extracts[th.string] = td.string
print(extracts)

# Dictionnaire de correspondence
correspondence = {
    "universal_ product_code (upc)": "UPC",
    "price_including_tax": "Price (incl. tax)",
    "price_excluding_tax": "Price (excl tax)",
    "number_available": "Avaibility"
    }
#for key in correspondence.keys():



'''



'''