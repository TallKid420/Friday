import re
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import networkx as nx

def remove_non_text(input_string):
  # Use a regular expression to match any character that is not a letter or a space
  pattern = re.compile(r'[^a-zA-Z\s\.]')
  # Replace all non-letter and non-space characters with an empty string
  output_string = pattern.sub('', input_string)
  return output_string

def summarize(text, question):
    x=0
    lq = question.split(' ')
    for i in lq:
        # logic to decide what it is asking

        # what is a () logic
        if i.lower() == "what" and lq[x+1] == "is" and lq[x+2] == "an" or i.lower() == "what" and lq[x+1] == "is" and lq[x+2] == "a":
            pattern = r'(.*\b(an '+lq[x+3]+r' is)\b.*)'
            match = re.search(pattern, text.lower())
            matches = re.findall(pattern, text.lower())
            print(matches)
        x=x+1
            

def scrape_info(topic):
    # Set up the list of websites to scrape
    websites = [
        "https://en.wikipedia.org/wiki/{}".format(topic)
    ]

    # Initialize an empty list to store the results
    results = []

    # Iterate over each website
    for website in websites:
        # Make a request to the website and retrieve the HTML content
        html_doc = requests.get(website).text
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_doc, 'html.parser')
        # Extract the relevant information from the website
        info = soup.get_text()
        # Add the information to the list of results
        results.extend(info)
        results = ''.join(results)
    # Return the list of results
    return results

text = scrape_info("Apple")
text = remove_non_text(text)
summary = summarize(text, "what is an apple")
print(summary)
