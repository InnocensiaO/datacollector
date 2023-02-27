from bs4 import BeautifulSoup
import requests
import psycopg2, psycopg2.extras
import json
from pandas.io.json import json_normalize
from selenium import webdriver
import re
import time
import pandas as pd
import csv

df = pd.read_csv('.csv')
    # print(df)
df2 = df['Wikipedia']
df3 = df2.dropna()
for i in (df3):
    # print(i)
    x = str(i)
    # print(x)
    pattern = "/wiki/"
    y = x.split(pattern, 1)[-1]
  


    parkname = y
    print(parkname)
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/{parkname}/daily/20210101/20211231"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"}

    response = requests.get(url, headers=headers).text
    # print(response)

    #print(source)
    # convert 'str' to Json
    wikijs = json.loads(response)
    print(wikijs)
    conn = psycopg2.connect(host="", dbname="", port="5432",
                            user="", password="")
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO table (json) VALUES(replace(convert_from(convert_to('{0}','LATIN1'),'UTF8'),'\\u0000','')::jsonb)".format(
            str(json.dumps(wikijs)).replace("'", "''")))
    conn.commit()
    conn.close()
    time.sleep(3)

