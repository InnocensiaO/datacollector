import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

opts = Options()
opts.add_argument("user-agent=[user-agent string]")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument("--headless")


df = pd.read_csv('.csv')
# print(df)
df2 = df['TripAdvisor']
df3 = df2.dropna()

tripreview = []
tripdate = []
tripreviewer = []
triplocation = []
triprating = []
trippark = []
tripparkid = []
tripuserlikes = []
tripcontrib = []
tripuserprofilelink = []

for i in (df3):
    # print(i)
    x = str(i)
    # print(x)
    pattern = "-Reviews-"
    y = x.split(pattern, 1)[0]
    # print(y)
    z = x.split(pattern, 1)[-1]
    # print(z)
    # p= y+"-Reviews-or"+str(j)+z
    # print(m)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    url = x
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    parkname = soup.find('h1', class_='biGQs _P fiohW eIegw').text
    print(parkname)
    # park=tripnameofpark.append(parkname.text)
    #park = parkname.text
    #print(park)
    #parkid='001'

    num_pages = soup.find('span', class_='yyzcQ')
    print(num_pages)
    # pag = num_pages.

    if num_pages is not None:
        # pag = num_pages
        pag = num_pages.text
        pag2 = pag.split(' ')
        # print(pag2)
        # print(type(pag2))
        end = pag2[-1]
        # print(type(end))
        # print(end)
        s = end.replace(',', '')
        pgt = int(s)
        pagestotal = pgt
        # print(pagestotal)

        multiples_10 = [n for n in range(1230, 2760) if n % 10 == 0]
        print(multiples_10)
    else:
        multiples_10 = [n for n in range(0, 1) if n % 10 == 0]

    #for j in range(1230, 2750, 10):
    for j in (multiples_10):

        if j ==1230:

            url2 = y + "-Reviews-or" +'-'+ str(j) + z
            k = url2.split(' ')
            #print(k)

            for m in k:
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                #url3 = m
                #print(url3)

                driver.get(m)
                time.sleep(1)
                #driver.find_element(By.XPATH,
                 #                   '//*[@id="tab-data-qa-reviews-0"]/div/div[1]/span/div/div[2]/div/div/span[2]/span/div/div/button').click()

                driver.execute_script("arguments[0].click();", WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-data-qa-reviews-0"]/div/div[1]/div/div/div[2]/div/div/div[2]/div/div/div/button'))))
                time.sleep(5)
                # click on all languages button
                driver.find_element(By.XPATH, '//*[@id="menu-item-all"]').click()
                time.sleep(5)

        else:

            #next = driver.find_element(By.XPATH, '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div[11]/div[1]/div/div[1]/div[2]/div/a').click()
            next=driver.execute_script("arguments[0].click();", WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div[11]/div[1]/div/div[1]/div[2]/div/a'))))

            #time.sleep(5)
            print(driver.current_url)


        soup = BeautifulSoup(driver.page_source, 'html.parser')
        #driver.quit()

        #reviewbox = soup.find_all('div', class_='_c')  # box for each reviews
        reviewbox = soup.find_all('div', class_='biGQs _P pZUbB KxBGd')
        reviewdatebox = soup.find_all('div', class_='biGQs _P pZUbB ncFvv osNWb')

        userinfobox = soup.find_all('div', class_='mwPje f M k')
        usercontrbox = soup.find_all('div', class_='JINyA')
        usernamebox = soup.find_all('div', class_='cjhIj')
        userratingbox = soup.find_all('div', class_='LbPSX')
        #userratingbox = soup.find_all('svg', class_='UctUV d H0')
        userlikesbox = soup.find_all('button', class_='BrOJk u j z _F wSSLS HuPlH Vonfv')
        userprofilelinkbox = soup.find_all('span', class_='WlYyy cPsXC dTqpp')
        userprofilelinkbox2 = soup.find_all('div', class_='bJyQA f u o')

        for review in reviewbox:
            reviewtext = review.find_all("span", class_="yCeTE")
            for review in reviewtext:
                print(review.text)
                tripreview.append(review.text)

        for reviewdate in reviewdatebox:
            print(reviewdate.text)
            tripdate.append(reviewdate.text)

        for username in userinfobox:
            usernametext = username.find_all('span', class_='biGQs _P fiohW fOtGX')
            for username in usernametext:
                #usernametext = username.find_all("a", class_='iPqaD _F G- ddFHE eKwUx btBEK fUpii')
                usernametext=username.find("a", attrs={"class": "BMQDV _F G- wSSLS SwZTJ FGwzt ukgoS"})
                print(username.text)
                tripreviewer.append(username.text)


        for userprofile in userinfobox:
            userprofiletext = userprofile.find_all('span', class_='biGQs _P fiohW fOtGX')
            for userprofile in userprofiletext:
                userprofiletext = userprofile.find("a", attrs={"class": "BMQDV _F G- wSSLS SwZTJ FGwzt ukgoS"}).get('href')
                print(userprofiletext)
                tripuserprofilelink.append(userprofiletext)


        for userprofilelocation in userinfobox:
            locations = userprofilelocation.find_all('div', class_='biGQs _P pZUbB osNWb')
            for userprofilelocation in locations:
                location = userprofilelocation.find('span')
                print(location.text)
                triplocation.append(location.text)

        for contributions in userinfobox:
            contribution = contributions.find('div', class_='biGQs _P pZUbB osNWb')
            print(contribution.text)
            tripcontrib.append(contribution.text)

        for userrating in userratingbox:
           rating = userrating.find_all('svg', class_='UctUV d H0')
           for userrating in rating:
               rate = userrating['aria-label']
               print(rate)
               triprating.append(rate)


        for userlike in userlikesbox:
            likes = userlike.find_all('span', class_='kLqdM')
            for userlike in likes:
                like = userlike.find_all('span', class_='biGQs _P FwFXZ')
                print(userlike.text)
                tripuserlikes.append(userlike.text)
                trippark.append(parkname)

        review_df = {'Date': tripdate,
                     'Review': tripreview,
                     'Reviewer': tripreviewer,
                     'Userprofilelink': tripuserprofilelink,
                     'Ratings': triprating,
                     'Userprofilelocation': triplocation,
                     'Reviewlikes': tripuserlikes,
                     'Number of contribution': tripcontrib,
                     'Park name':trippark
                     }
        df = pd.DataFrame.from_dict(review_df, orient='index')
        df = df.transpose()
        df.to_csv(parkname+'download.csv', index=False, encoding="utf-8")

