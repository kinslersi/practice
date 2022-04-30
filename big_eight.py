import requests
from bs4 import BeautifulSoup
import pandas as pd

data=[]
r=requests.get("http://chart.capital.com.tw/Chart/TWII/TAIEX11.aspx")
soup=BeautifulSoup(r.text,"html.parser")
tables=soup.find_all("table",attrs={"cellpadding":"2"})    # 利用大小表格的差別，取出兩個小表格
for table in tables:
    trs=table.find_all("tr")
    for tr in trs:
        date,value,price=[td.text for td in tr.find_all("td")]
        if date=="日期":     # 去掉第一行開頭
            continue
        data.append([date,value,price])   # 以每一行為一個單位
print(data)

df=pd.DataFrame(data,columns=["日期","買賣超金額","台指期"])   # 轉為dataframe,手動輸入column name
df.to_csv("big_eight.csv")
df.to_html("big_eight.html")
df.to_excel("big_eight.xlsx")