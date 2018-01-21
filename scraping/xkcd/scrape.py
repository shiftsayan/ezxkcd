from bs4 import BeautifulSoup
import requests
import shutil
import glob
from os import listdir
from os.path import isfile, join
import urllib.request, json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
import random
import bisect
import webbrowser

LATEST_XKCD = 1944

analyzer = SentimentIntensityAnalyzer()

def scrape_xkcd_comics(c_range):

  result = []

  for c in c_range:

    if c == 404: continue

    xkcd = "https://xkcd.com/" + str(c) + "/info.0.json"
    print("Scraping xkcd comic " + str(c) + " from " + xkcd[:-11])

    with urllib.request.urlopen(xkcd) as url:
        text = url.read()
        data = json.loads(text)
        transcript = data["transcript"]
        vs = analyzer.polarity_scores(transcript)
        result.append([vs["compound"], c,])

  return sorted(result, key = lambda x: x[0])

def binary_search(data, val):
    highIndex = len(data)-1
    lowIndex = 0
    while highIndex > lowIndex:
            index = (highIndex + lowIndex) / 2
            sub = data[index][0]
            if data[lowIndex][0] == val:
                    return lowIndex
            elif sub == val:
                    return index
            elif data[highIndex][0] == val:
                    return highIndex
            elif sub > val:
                    if highIndex == index:
                            return random.choice([highIndex, lowIndex])
                    highIndex = index
            else:
                    if lowIndex == index:
                            return random.choice([highIndex, lowIndex])
                    lowIndex = index
    return random.choice([highIndex, lowIndex])

all_xkcds = scrape_xkcd_comics(range(1, LATEST_XKCD + 1))
all_scores = []

for xkcd in all_xkcds:
    all_scores.append(xkcd[0])

while True:
    score = float(input("Enter a real number between -1 and 1: "))
    if not -1 <= score <= 1: continue

    try:
        comic = all_xkcds[bisect.bisect(all_scores, score)][1]
        url = "https://xkcd.com/" + str(comic) + "/"
        webbrowser.open(url)
    except:
        pass
