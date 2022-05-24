import requests
from bs4 import BeautifulSoup
import re

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

paragraphe = soup.findAll('p', {})
extracts["product_description"] = paragraphe[3].string

category = soup.find("a", href=re.compile("/books/"))
extracts["category"] = category.string

review_rating = soup.find(class_=re.compile("star-rating"))
extracts[review_rating['class'][0]] = review_rating['class'][1]

image_tag = soup.find('div', class_= "item active")
img_tag = image_tag.img
image_url = img_tag['src']
extracts["image_url"] = image_url


# Extraction données du tableau html
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