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
    wikilinkedits = f"https://wikimedia.org/api/rest_v1/metrics/edits/per-page/en.wikipedia.org/{parkname}/all-editor-types/daily/20210101/20211231"
    # print(wikilinkedits)
    source = requests.get(wikilinkedits).text
    #print(source)
    # convert 'str' to Json
    wikijs = json.loads(source)
    print(wikijs)
    conn = psycopg2.connect(host="", dbname="", port="5432",
                            user="", password="")
    cur = conn.cursor()
    # SQL = "INSERT INTO tweets_stream_ne_I (json) values ('"+encoded+"')"
    cur.execute(
        "INSERT INTO table (json) VALUES(replace(convert_from(convert_to('{0}','LATIN1'),'UTF8'),'\\u0000','')::jsonb)".format(
            str(json.dumps(wikijs)).replace("'", "''")))
    conn.commit()
    conn.close()
    time.sleep(2)

