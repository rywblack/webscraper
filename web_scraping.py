from bs4 import BeautifulSoup
import requests
import re

def printPage(inp,url,genres):
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    ol = doc.find("ol")
    for li in ol.find_all("li"):
        print("")
        print(li.find("h3").find("a").string)
        print(f"Price: {li.find(class_="product_price").find(class_="price_color").string.replace('Â', ' ').strip()}")
        print(li.find(class_="product_price").find(class_="instock availability").get_text(strip=True))

    if doc.find(class_="current") is not None:
        print("")
        print(doc.find(class_="current").get_text(strip=True))
        print("")
        inp2 = input("What page number would you like to go to? ")
        finalPageNum = int(doc.find(class_="current").get_text(strip=True)[len(doc.find(class_="current").get_text(strip=True))-1])
        def checkPageNum(inp,inp2,finalPageNum,genres):
            try:
                inp2 = int(inp2)
                finalPageNum = int(finalPageNum)
            except ValueError:
                inp2 = -1 
            if int(inp2) < 1 or int(inp2) > finalPageNum or not isinstance(inp2,int):
                inp2 = input("invalid page number, please try again: ")
                checkPageNum(inp,inp2,finalPageNum,genres)
            else:
                printPage(inp,f"https://books.toscrape.com/catalogue/category/books/{inp.replace(' ', '-')}_{genres.index(inp)+2}/page-{inp2}.html",genres)
        
        checkPageNum(inp,inp2,finalPageNum,genres)



print("WELCOME, PLEASE PICK A GENRE FROM BELOW:")
print("")

url = f"https://books.toscrape.com/index.html"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

parent_ul = doc.find(class_="nav nav-list")
grandchild_ul = parent_ul.find("ul")

genres = []
for li in grandchild_ul.find_all("li"):
    genres.append(li.get_text(strip=True))

print(", ".join(genres))

print("")

inp = input()

genres = list(map(lambda x: x.lower(),genres))
inp = inp.lower()

if inp in genres:
    url = f"https://books.toscrape.com/catalogue/category/books/{inp.replace(' ', '-')}_{genres.index(inp)+2}/index.html"
    printPage(inp,url,genres)
else:
    print("genre not found")


