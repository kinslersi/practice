import requests
from bs4 import BeautifulSoup
from pprint import pprint

re=requests.get("https://chart.stock-ai.com/history?symbol=AAPL&resolution=D&from=1611665528&to=1650977588")
data=re.json() 
zipped=zip(data["t"],data["o"],data["h"],data["l"],data["o"],data["v"])
pprint(list(zipped))