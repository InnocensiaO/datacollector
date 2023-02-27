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




df = pd.read_csv('links.csv')
    # print(df)
df2 = df['Yelp']
df3 = df2.dropna()
for i in (df3):
    # print(i)
    x = str(i)
    print(x)

    for i in df3:
        url = x + "&start="


        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        parkname = soup.find('h1', class_='css-1se8maq')

        park = parkname.text
        print(park)

        yelppark = []
        yelpdate = []
        yelpreview = []
        yelpreviewer = []
        yelprating = []
        yelplocation = []
        yelpid = []
        yelpuserprofilelink = []

        # start = 0
        pagebox = soup.find('div', class_='border-color--default__09f24__NPAKY text-align--center__09f24__fYBGO')
        for pg in pagebox:
            num_pages = soup.find('span', class_='css-chan6m')
            print(pg.text)
            pag = pg.text
            pag2 = pag.split(' ')
            print(pag2)
            # print(type(pag2))
            end = pag2[-1]
            pagestotal = int(end)
            # print(pagestotal)
            totalnumofpages = (pagestotal) * 10
            print(totalnumofpages)
            multiples_10 = [n for n in range(0, totalnumofpages) if n % 10 == 0]

            print(multiples_10)

            for j in (multiples_10):
                url3 = url +str(j)+'&sort_by=date_desc'


                k = url3.split(' ')
                print(k)

                for m in k:
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                    driver.get(m)
                    time.sleep(1)

                    #driver.find_element(By.XPATH,
                                       #'//*[@id="reviews"]/section/div[2]/div/div[4]/div/div[1]/div/div[1]/div/span/span/button').click()

                    #time.sleep(5)

                    #driver.find_element(By.XPATH, '//*[@id="reviews"]/section/div[2]/div/div[4]/div[1]/div[1]/div/div[1]/div/span/div/menu/div/div[2]/button/div/div/p').click()
                    #time.sleep(5)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    driver.quit()

                    totalreviews = soup.find('span', class_='css-1fdy0l5')
                    # numrev=int(totalreviews.text)

                    x=='comment__09f24__gu0rG css-qgunke'
                    reviewbox = soup.find_all('p', class_='comment__09f24__gu0rG css-qgunke')  # box for each reviews
                    reviewdatebox = soup.find_all('div',
                                                  class_='margin-t1__09f24__w96jn margin-b1-5__09f24__NHcQi border-color--default__09f24__NPAKY')

                    userinfobox = soup.find_all('div',
                                                class_='review__09f24__oHr9V border-color--default__09f24__NPAKY')

                    userlocationbox = soup.find_all('div',
                                                    class_='review__09f24__oHr9V border-color--default__09f24__NPAKY')

                    userratingbox = soup.find_all('div',
                                                  class_='review__09f24__oHr9V border-color--default__09f24__NPAKY')

                    for review in reviewbox:
                        reviewtext = review.find_all("span", class_="raw__09f24__T4Ezm")
                        for review in reviewtext:
                            print(review.text)
                            yelpreview.append(review.text)


                    for reviewdate in reviewdatebox:
                       dateofreview = reviewdate.find_all("div",
                                                           class_="arrange__09f24__LDfbs gutter-1__09f24__yAbCL vertical-align-middle__09f24__zU9sE border-color--default__09f24__NPAKY")
                       for reviewdate in dateofreview:
                          dateofreview = reviewdate.find_all("span", class_="css-chan6m")
                          print(reviewdate.text)
                          if 'Previous review' not in reviewdate.text:
                              yelpdate.append(reviewdate.text)


                    for username in userinfobox:
                        usernametext = username.find_all('span', class_='fs-block css-ux5mu6')
                        for username in usernametext:
                            if not None:
                                usernametext = username.find_all("a", class_='css-1m051bw')
                                print(username.text)
                                yelpreviewer.append(username.text)
                            else:
                                yelpreviewer.append('Null')

                    for userprofile in userinfobox:
                        userprofiletext = userprofile.find_all('span', class_='fs-block css-ux5mu6')
                        for userprofile in userprofiletext:
                            if not None:
                                userprofiletext = userprofile.find("a", attrs={
                                "class": "css-1m051bw"}).get('href')
                                print(userprofiletext)
                                yelpuserprofilelink.append(userprofiletext)
                            else:
                                yelpuserprofilelink.append('Null')

                    for userprofilelocation in userlocationbox:
                        location = userprofilelocation.find_all('span', class_='css-qgunke')
                        for userprofilelocation in location:
                            if not None:
                                print(userprofilelocation.text)
                                yelplocation.append(userprofilelocation.text)
                            else:
                                yelplocation.append('Null')

                    for userrating in userratingbox:
                        print(userrating.select('[aria-label*=rating]')[0]['aria-label'])
                        yelprating.append(userrating.select('[aria-label*=rating]')[0]['aria-label'])

                        yelppark.append(park)
                        print(len(yelpreview), len(yelpdate), len(yelpreviewer), len(yelplocation), len(yelprating))

                    review_df = {
                        'Date': yelpdate,
                        'Review': yelpreview,
                        'Reviewer': yelpreviewer,
                        'useprofilelink': yelpuserprofilelink,
                        'Ratings': yelprating,
                         'Userprofilelocation': yelplocation,
                        'Parkname': yelppark}
                    df=pd.DataFrame.from_dict(review_df, orient='index')
                    df = df.transpose()

                    df.to_csv(park + 'downloaded.csv', index=False, encoding="utf-8")
                    time.sleep(5)





