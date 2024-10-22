from bs4 import BeautifulSoup
import requests
import re
import os

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
        inp2 = input("What page number would you like to go to? (type 'return' to return to the genre selection screen) ")
        finalPageNum = int(doc.find(class_="current").get_text(strip=True)[len(doc.find(class_="current").get_text(strip=True))-1])
        def checkPageNum(inp,inp2,finalPageNum,genres):
            if inp2.lower() == 'return':
                os.system('clear')
                homeScreen()
            try:
                inp2 = int(inp2)
                finalPageNum = int(finalPageNum)
            except ValueError:
                inp2 = -1 
            if int(inp2) < 1 or int(inp2) > finalPageNum or not isinstance(inp2,int):
                inp2 = input("invalid page number, please try again: ")
                checkPageNum(inp,inp2,finalPageNum,genres)
            else:
                os.system('clear')
                printPage(inp,f"https://books.toscrape.com/catalogue/category/books/{inp.replace(' ', '-')}_{genres.index(inp)+2}/page-{inp2}.html",genres)
        
        checkPageNum(inp,inp2,finalPageNum,genres)
    else:
        print("")
        inp2 = input("Type 'return' to return to the genre selection screen: ")
        inp2 = inp2.lower()
        def checkReturn(inp2):
            if inp2 != "return":
                inp2 = input("invalid input, please try again: ")
                checkReturn(inp2)
            else:
                os.system('clear')
                homeScreen()
        checkReturn(inp2)


def homeScreen():

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
    def checkGenre(inp):
        if inp in genres:
            url = f"https://books.toscrape.com/catalogue/category/books/{inp.replace(' ', '-')}_{genres.index(inp)+2}/index.html"
            os.system('clear')
            printPage(inp,url,genres)
        else:
            inp = input("genre not found, please try again: ")
            checkGenre(inp)
    checkGenre(inp)


def main():
    homeScreen()

if __name__ == "__main__":
    main()
