import requests
from bs4 import BeautifulSoup

def get_summary(query):
  # Make a GET request to the Google search page
  res = requests.get(f'https://www.google.com/search?q={query}')

  # Parse the HTML content of the page
  soup = BeautifulSoup(res.text, 'html.parser')

  # Find the first search result on the page
  result = soup.find('div', class_='VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf')

  # Extract the URL of the page
  url = result.find('a')['href']

  # Make a GET request to the URL of the page
  res = requests.get(url)

  # Parse the HTML content of the page
  soup = BeautifulSoup(res.text, 'html.parser')

  # Extract the summary of the page
  summary = soup.find('p').text

  return summary

get_summary("apples")