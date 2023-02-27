import psycopg2
import json
import sys

import requests
import pandas as pd
import time


pd.options.display.float_format = '{:.2f}'.format
df = pd.read_csv('.csv')
#print(df)
errorboundlinks=[]

# Create an empty list
bounds_list = []
bounds_list = df['bounding'].tolist() #search twitter using the boundary coordinates in this list


for number, i in enumerate(bounds_list):
    print(number,i)


    def search_endpoint_connect(bearer_token, query, st, et, next_token):
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        query_params = {
            'query': query,
            'start_time': st,
            'end_time': et,
            'max_results': 500,
            'tweet.fields': 'id,text,author_id,created_at,geo,lang,source',
            'user.fields': 'created_at,id,location,name,username',
            'place.fields': 'id,name,full_name,country,country_code,geo,place_type',
            'expansions': 'author_id,geo.place_id'
        }

        if (next_token is not None):
            url = "https://api.twitter.com/2/tweets/search/all?next_token={}".format(next_token)
        else:
            url = "https://api.twitter.com/2/tweets/search/all"

        response = requests.request("GET", url, params=query_params, headers=headers)

        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

        return response.json()


    def main(bearer_token, n, sq, st, et):
        rl_count = 0
        count = 0
        flag = True
        first = True

        try:
            while flag:


                if rl_count == 250:
                    time.sleep(3600)
                    print('Rate limit cooldown 60 mins.')

                if count >= n and n != 0:
                    break
                if not first:
                    json_response = search_endpoint_connect(bearer_token, sq, st, et, next_token)
                else:
                    json_response = search_endpoint_connect(bearer_token, sq, st, et, next_token=None)

                result_count = json_response['meta']['result_count']
                if 'next_token' in json_response['meta']:
                    next_token = json_response['meta']['next_token']

                    if result_count is not None and result_count > 0 and next_token is not None:
                        encoded = json_response
                        conn = psycopg2.connect(host="", dbname="", port="5432",
                                                user="", password="")
                        cur = conn.cursor()
                        # SQL = "INSERT INTO tweets_stream_ne_I (json) values ('"+encoded+"')"
                        SQL = "INSERT INTO table(json)VALUES(replace(convert_from(convert_to('{0}','LATIN1'),'UTF8'),'\\u0000','')::jsonb)".format(
                            str(json.dumps(encoded)).replace("'", "''"))
                        # print encoded
                        cur.execute(SQL)
                        conn.commit()
                        conn.close()
                        time.sleep(10)
                        count += result_count
                        print('Tweets downloaded: ' + str(count))
                else:
                    flag = False
                rl_count += 1
                first = False
                time.sleep(10)

        except Exception as e:

            #print(number, i)
            print(e)

            errorboundlinks.append(i)
            errorboundlinksdict={'links': errorboundlinks}
            errorboundlinksdf = pd.DataFrame.from_dict(errorboundlinksdict, orient='index')
            errorboundlinksdf = errorboundlinksdf.transpose()
            errorboundlinksdf.to_csv('.csv', index=False, encoding="utf-8") #print errors
            pass
            time.sleep(5)


    # Enter your bearer token
    bearer_token = ''

    # Set number of tweets to be downloaded. Enter 0 for no limits
    no_of_tweets = 0

    # Specify the name of the output csv file. Do not include .csv
    # file_name = 'downloaded_tweets'
    search_query = '(has:geo)'+ str(i)

    # print(type(search_query))

    # Set the beginning date and time in YYYY-MM-DDTHH:MM:SSZ format
    start_time = "2020-02-28T23:59:59Z"

    # Set the ending date and time in YYYY-MM-DDTHH:MM:SSZ format
    end_time = "2020-05-01T01:01:59.9Z"

    main(bearer_token, no_of_tweets, search_query, start_time, end_time)




