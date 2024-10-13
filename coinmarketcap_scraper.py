from bs4 import BeautifulSoup
import requests

url = "https://coinmarketcap.com/"
result = requests.get(url).text
doc = BeautifulSoup(result, "html.parser")

tbody = doc.tbody
#trs = tbody.contents
prices = {}

td_elements = doc.find_all('td')

non_empty_spans = []
plist = []
for td in td_elements:
    span = td.find('span')
    p = td.find('p', class_="sc-65e7f566-0 iPbTJf coin-item-name")
    if span and span.get_text(strip=True) and not span.attrs:  
        non_empty_spans.append(span.string)
    if p and p.get_text(strip=True):
        plist.append(p.string)

for i in range(0,len(non_empty_spans)):
    prices[plist[i]]=non_empty_spans[i]

print(prices)


