import requests
from bs4 import BeautifulSoup

re=requests.get("https://tw.stock.yahoo.com/us/q?s=CL=F")
soup=BeautifulSoup(re.text,"html.parser")
table=soup.find_all("table")[3]   # 不設定關鍵字，直接找第幾個表格
price=table.find_all("td")[12]   # 成交價
buy_price=price.find_next("td")  # 賣進, find_next找下一個
sell_price=buy_price.find_next("td") # 賣出
print(price.text)
print(buy_price.text)
print(sell_price.text)