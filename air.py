import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re

r=requests.get("https://airtw.epa.gov.tw/json/camera_ddl_pic/camera_ddl_pic_2022042716.json?t=1651051286948")
data=r.json()   
for d in data:
    name=d["Name"]
    try:
        site_name=re.search(r"(.+)\(AQI=(\d+)",name).group(1)
        aqi=re.search(r"(.+)\(AQI=(\d+)",name).group(2)
        print(site_name,aqi)
    except AttributeError:
        pass