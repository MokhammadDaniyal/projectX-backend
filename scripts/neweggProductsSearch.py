#!/usr/bin/python -u

import sys
import os
import requests
import urllib
from bs4 import BeautifulSoup
import json
import time
from scraper_api import ScraperAPIClient

isUseScraperAPI = True


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


class Item:
    def __init__(self, price, title, link, image):
        self.price = price
        self.title = title
        self.link = link
        self.image = image

    def to_dict(self):
        return {"title": self.title, "price": self.price, "link": self.link, "image": self.image}


name = sys.argv[1].replace(" ", "+")
count = int(sys.argv[2])
# print("Product name: " + name)
isSamePage = False
pageNo = 1
lastPage = None
itemList = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
}


def useScraperAPI(URL):
    client = ScraperAPIClient('d249e87aac326eaa5e728aafaa319d10')
    page = client.get(url=URL)
    page = BeautifulSoup(page.text, 'html.parser')
    return page


def usePyRequest(URL):
    page = requests.get(URL, allow_redirects=False, headers=headers)
    page = BeautifulSoup(page.text, 'html.parser')
    return page


def exctractProductsOnPage(page):
    pagination = page.find('div', class_="list-tool-pagination")
    paginationText = pagination.find(
        'span', class_='list-tool-pagination-text')
    count = paginationText.find('strong').text.split("/", 1)[1]
    return int(count)


def extractProductInfo(itemCell):
    itemTitle = itemCell.find('a', class_='item-title')
    title = itemTitle.text.strip()
    link = itemTitle['href'].replace(" ", "%20")
    imageContainer = itemCell.find('a', class_='item-img')
    image = imageContainer.find('img')['src']
    price_strong = itemCell.find(
        'li', class_='price-current').find('strong').text.strip()
    price_sup = itemCell.find(
        'li', class_='price-current').find('sup').text.strip()
    item = Item(price_strong+price_sup, title, link, image)
    return item


URL = 'https://www.newegg.ca/p/pl?d='+name+'&Page=' + str(pageNo)
if (isUseScraperAPI):
    page = useScraperAPI(URL)
else:
    page = usePyRequest(URL)
    if (page.status_code == 302):
        sys.stderr.write("STATUS CODE 302 REDIRECT PAGE, MGHT BE CAPPTCHA")
        page = useScraperAPI(URL)
        isUseScraperAPI = True
pageMaxCount = exctractProductsOnPage(page)
while pageNo <= pageMaxCount:
    # print(pageNo)
    if count <= 0:
        break
    job_elems = page.find_all('div', class_='item-cell')
    for job_elem in job_elems:
        if count <= 0:
            break
        item = extractProductInfo(job_elem)
        itemList.append(item)
        count = count - 1
        # print(json.dumps(item.__dict__))
    pageNo += 1


results = [item.to_dict() for item in itemList]

for i, item in enumerate(itemList):
    sys.stdout.write(json.dumps(item.__dict__))
    if not i == len(itemList) - 1:
        sys.stdout.write(',')
    # sys.stdout.flush()
    # time.sleep(1)


# for 5 in results:
#   json_string = json.dumps(item)
#   sys.stdout.write()
#   sys.stdout.flush()
#   time.sleep(0.05)

# sys.stdout.write(json.dumps(results))
# sys.stdout.flush()
# print(json_string)
