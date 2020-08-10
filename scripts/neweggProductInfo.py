import sys
import os
import requests
import urllib
from bs4 import BeautifulSoup
import json
import time
from copy import deepcopy
from scraper_api import ScraperAPIClient

isUseScraperAPI = False

productLink = sys.argv[1]
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

def extractProductInfo(page):
    specsContainer = page.find(id='Specs')
    specs = specsContainer.find_all('fieldset')
    specTable = []
    for fieldset in specs:
        specDict = {}
        title = fieldset.find('h3', class_='specTitle').text
        specDict["title"]= title
        specDict["specs"] = []
        specRow = fieldset.find_all('dl')
        for row in specRow:
            specName = row.find('dt').text
            specDesc = row.find('dd').text
            obj = {}
            obj[specName] = specDesc
            specDict["specs"].append(deepcopy(obj))
        specTable.append(deepcopy(specDict))
    sys.stdout.write(json.dumps(specTable))

page = usePyRequest(productLink)
extractProductInfo(page)
