import requests
from datetime import datetime as dt
import pandas as pd
import time


# we use this function to convert responses to dataframes
def df_from_response(res):
    # initialize temp dataframe for batch of data in response
    df = pd.DataFrame()

    # loop through each post pulled from res and append to df
    for post in res.json()['data']['children']:

        df = df.append({
            'subreddit': post['data']['subreddit'],
            'author': post['data']['author'],
            'domain': post['data']['domain'],
            'num_comments': post['data']['num_comments'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'ups': post['data']['ups'],
            'downs': post['data']['downs'],
            'score': post['data']['score'],
            'link_flair_css_class': post['data']['link_flair_css_class'],
            'created_utc': dt.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'id': post['data']['id'],
            'kind': post['kind']
        }, ignore_index=True)
    return df

def serve_cycle(iter_dict):
    params = iter_dict["params"]
    SUBREDDIT = iter_dict["SUBREDDIT"]
    SUB_TYPE = iter_dict["SUB_TYPE"]
    fullname_for_before_movement = None
    for i in range(iter_dict["cur_iter"], HUNDREDS):
        # make request
        res = requests.get(f"https://oauth.reddit.com/r/{SUBREDDIT}/{SUB_TYPE}",
                           headers=headers,
                           params=params)

        # get dataframe from response
        new_df = df_from_response(res)
        # take the final row (oldest entry)
        print(i, len(new_df))
        if i == 0 and "before" not in params.keys():
            row = new_df.iloc[0]
            fullname_for_before_movement = row['kind'] + '_' + row['id']
            row = new_df.iloc[len(new_df) - 1]
            fullname = row['kind'] + '_' + row['id']
            params['after'] = fullname
        if len(new_df) < params["limit"]:
            #print(new_df)
            #print(res.text)
            print(len(new_df), "<=", params["limit"])
            iter_dict["cur_iter"] = i
            params.pop("after", 2000)
            if fullname_for_before_movement:
                params["before"] = fullname_for_before_movement
            params["limit"] = 3
            iter_dict["params"] = params
            print("break:", params, iter_dict)

            break



        if "after" in params.keys():
            row = new_df.iloc[len(new_df) - 1]
            fullname = row['kind'] + '_' + row['id']
            params['after'] = fullname
        if "before" in params.keys():
            row = new_df.iloc[0]
            fullname = row['kind'] + '_' + row['id']
            params['before'] = fullname
        # create fullname

        print(fullname)

        # append new_df to data
        #data = data.append(new_df, ignore_index=True)
        new_df.to_csv(f"../data/r_{SUBREDDIT}_{SUB_TYPE}_" + NOW[:4] + ".csv", mode="a")
        print(res.headers['x-ratelimit-remaining'],
                res.headers['x-ratelimit-used'],
                res.headers['x-ratelimit-reset'], dt.now())
        time.sleep(2)

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth('0bRC0ZO6kEbkQetQomwU4g', 'lJrmM8jymrRZgOJcmEg9nXALnuh_KQ')

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': 'Koba_69',
        'password': 'Ko1969ba'}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'python:kokEternity script:v1.0 (by /u/Koba_69)'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

#===================================
#data = pd.DataFrame()



params = {'limit': 100}
iterations = [{"cur_iter": 0, "SUBREDDIT": "wallstreetbets", "SUB_TYPE": "top", "params": {'limit': 100}},
            {"cur_iter": 0, "SUBREDDIT": "wallstreetbets", "SUB_TYPE": "rising", "params": {'limit': 100}},
            {"cur_iter": 0, "SUBREDDIT": "wallstreetbets", "SUB_TYPE": "hot", "params": {'limit': 100}},
            {"cur_iter": 0, "SUBREDDIT": "wallstreetbets", "SUB_TYPE": "new", "params": {'limit': 100}},
              {"cur_iter": 0, "SUBREDDIT": "BBIG", "SUB_TYPE": "top", "params": {'limit': 100}},
              {"cur_iter": 0, "SUBREDDIT": "BBIG", "SUB_TYPE": "rising", "params": {'limit': 100}},
              {"cur_iter": 0, "SUBREDDIT": "BBIG", "SUB_TYPE": "hot", "params": {'limit': 100}},
              {"cur_iter": 0, "SUBREDDIT": "BBIG", "SUB_TYPE": "new", "params": {'limit': 100}},
            {"cur_iter": 0, "SUBREDDIT": "Superstonk", "SUB_TYPE": "top", "params": {'limit': 100}},
            {"cur_iter": 0, "SUBREDDIT": "Superstonk", "SUB_TYPE": "rising", "params": {'limit': 100}},
            {"cur_iter": 0, "SUBREDDIT": "Superstonk", "SUB_TYPE": "hot", "params": {'limit': 100}},
            {"cur_iter": 0, "SUBREDDIT": "Superstonk", "SUB_TYPE": "new", "params": {'limit': 100}},
              {"cur_iter": 0, "SUBREDDIT": "amcstock", "SUB_TYPE": "top", "params": {'limit': 100}},
              {"cur_iter": 0, "SUBREDDIT": "amcstock", "SUB_TYPE": "rising", "params": {'limit': 100}},
              {"cur_iter": 0, "SUBREDDIT": "amcstock", "SUB_TYPE": "hot", "params": {'limit': 100}},
              {"cur_iter": 0, "SUBREDDIT": "amcstock", "SUB_TYPE": "new", "params": {'limit': 100}},
              {"cur_iter": 0, "SUBREDDIT": "KOSSstock", "SUB_TYPE": "top", "params": {'limit': 100}},
              {"cur_iter": 0, "SUBREDDIT": "KOSSstock", "SUB_TYPE": "rising", "params": {'limit': 100}},
              {"cur_iter": 0, "SUBREDDIT": "KOSSstock", "SUB_TYPE": "hot", "params": {'limit': 100}},
              {"cur_iter": 0, "SUBREDDIT": "KOSSstock", "SUB_TYPE": "new", "params": {'limit': 100}},
              {"cur_iter": 0, "SUBREDDIT": "CLOV", "SUB_TYPE": "top", "params": {'limit': 100}},
              {"cur_iter": 0, "SUBREDDIT": "CLOV", "SUB_TYPE": "rising", "params": {'limit': 100}},
              {"cur_iter": 0, "SUBREDDIT": "CLOV", "SUB_TYPE": "hot", "params": {'limit': 100}},
              {"cur_iter": 0, "SUBREDDIT": "CLOV", "SUB_TYPE": "new", "params": {'limit': 100}}
              ]



# loop through 10 times (returning 1K posts)
NOW = str(dt.now())
HUNDREDS = 15000000
ind = 0
while True:
    NOW = str(dt.now())
    serve_cycle(iterations[ind])
    ind = (ind + 1) % len(iterations)
    time.sleep(3)




