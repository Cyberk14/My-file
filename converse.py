import requests
from bs4 import BeautifulSoup

url = "https://www.reuters.com/markets/"
r = requests.get(url)

soup = BeautifulSoup(r.text, "html-parser")

print(r)
print("====================================")
print(soup)