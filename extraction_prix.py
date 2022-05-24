import requests
from bs4 import BeautifulSoup

recherche = ["universal_ product_code (upc)", "title", "price_including_tax",
    "price_excluding_tax", "number_available", "product_description",
    "category", "review_rating", "image_url"
    ]

print(recherche)

# Script extraction des informations  de la page produit
product_page_url = ("http://books.toscrape.com/catalogue/a-light-in-the"
                    "-attic_1000/index.html")
page = requests.get(product_page_url)
soup = BeautifulSoup(page.content, 'html.parser')

title = soup.find("li", class_="active")
print(title.string)

#extraction données du tableau html
trs = soup.find_all("tr")
print(trs)
extracts = {}
for tr in trs:
    th = tr.find("th")
    td = tr.find("td")
    extracts[th.string] = td.string
print(extracts)

title = soup.find("li", class_="active")
print(title.string)
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