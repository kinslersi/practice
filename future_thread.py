from __future__ import unicode_literals
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import json
import os
import time


def crawl(date):
    print("crawling", date.strftime("%Y/%m/%d"))
    r = requests.get(
        "https://www.taifex.com.tw/cht/3/futContractsDate?queryDate={}%2F{}%2F{}".format(date.year, date.month,
                                                                                         date.day))
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, "html.parser")
    else:
        print("connection error")
    try:
        table = soup.find("table", class_="table_f")
        trs = table.find_all("tr")
        data = {}
        for row in trs[3:]:
            ths = row.find_all("th")
            cells1 = [th.text.strip() for th in ths]
            tds = row.find_all("td")
            cells2 = [td.text.strip() for td in tds]
            if len(cells1) == 3:
                product = cells1[1]
                row_data = cells1[1:] + cells2
            else:
                row_data = [product] + cells1 + cells2
            if cells1[0] == "期貨小計":
                break
            convert = [int(d.replace(",", "")) for d in row_data[2:]]
            row_data = row_data[:2] + convert
            headers = ['商品', '身份別', '交易多方口數', '交易多方金額', '交易空方口數', '交易空方金額', '交易多空淨口數', '交易多空淨額', '未平倉多方口數', '未平倉多方金額',
                       '未平倉空方口數', '未平倉空方金額', '未平倉淨口數', '未平倉多空淨額']
            product = row_data[0]
            who = row_data[1]
            content = {headers[i]: row_data[i] for i in range(2, len(headers))}
            if product not in data:
                data[product] = {who: content}
            else:
                data[product][who] = content

            json_str = json.dumps(data, ensure_ascii=False)
            now = os.getcwd()
            abs_filepath = os.path.join(now, date.strftime("%Y%m%d") + ".json")
            with open(abs_filepath, "w") as f:
                f.write(json_str)
    except AttributeError:
        print("no data for", date.strftime("%Y/%m/%d"))

    


start = time.time()
date = datetime.today()
list_date = []
while True:
    list_date.append(date)
    date = date - timedelta(days=1)
    if date < datetime.today() - timedelta(days=720):
        break
with ThreadPoolExecutor() as executer:
    for n in list_date:
        executer.submit(crawl, n)
end = time.time()
print("take", end - start, "sec")