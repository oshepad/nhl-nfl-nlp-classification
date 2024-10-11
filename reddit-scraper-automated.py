# Imports
import pandas as pd
import requests
import time
import getpass

# Welcome prompt to gather credentials
print('Welcome to Reddit Scraper.  In order to use the model we need to \
collect some credentials. \
\nPlease provide your reddit username, password, client id, client secret,\
and user agent. \
\nThese will be stored in a json file so that you can use the model.\
\nThe client id is provided underneath the apps name.\
\nThe client secret is provided in the developped apps edit menu.\
\nThe user agent is a name that Reddit uses to track usage.')

username = getpass.getpass(prompt='Please enter username: ')
password = getpass.getpass(prompt='Please enter password: ')
client_id = getpass.getpass(prompt='Please enter client_id: ')
client_secret = getpass.getpass(prompt='Please enter client_secret: ')
user_agent = getpass.getpass(prompt='Please enter user agent: ')
subreddit_1 = input('What subreddit would you like to start with: ')
subreddit_2 = input('What other subreddit are you interested in: ')
subreddits = [subreddit_1, subreddit_2]

# Authenticate credentials to request access token
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
data = {'grant_type': 'password', 'username': username, 'password': password}
headers = {'User-Agent': user_agent + '/1.1.1'}

# Make request for token
res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth,
    data=data, headers=headers)

# Get token
token = res.json()['access_token']
headers['Authorization'] = f'bearer {token}'
requests.get('https://oauth.reddit.com/api/v1/me', 
             headers=headers).status_code == 200

# Initial subreddit scrapes and creating transaction log

for subreddit in subreddits:    
    base_url = 'https://oauth.reddit.com/r/'
    res = requests.get(base_url+subreddit, headers=headers)
    
    # Initial scrape from initial response
    postings = []
    for i in range(len(res.json()['data']['children'])):
        posting = []
        posting.append(time.ctime())
        posting.append((res.json()['data']['children'][i]['data']['name']))
        posting.append((res.json()['data']['children'][i]['data']['title']))
        posting.append((time.ctime(res.json()['data']['children'][i]
                                   ['data']['created_utc'])))
        posting.append((res.json()['data']['after']))
        posting.append(subreddit)
        postings.append(posting)
    
    pull = pd.DataFrame(postings, 
                        columns=['time_pulled', 'fullname', 'titles', 
                                 'times_created', 'anchors', 'subreddit'])
    pull['times_created'] = pd.to_datetime(pull['times_created'])
    pull.sort_values(by=['times_created'], inplace=True, ascending=False)
    
    # Transaction log
    transactions = []
    anchor = res.json()['data']['after']
    total_td = len(pull)
    transaction = [subreddit, len(pull), total_td, time.ctime(), anchor]
    transactions.append(transaction)
    transactions = pd.DataFrame(transactions, 
                                columns=['subreddit', 'pulled_postings',
                                          'total_postings', 
                                          'times_created', 'anchor'])

    # Write to csv file
    pull.to_csv('./data/' + subreddit + '_pulls.csv', index=False, mode='a')
    transactions.to_csv('./data/' + subreddit + '_transaction_log.csv', 
                        index=False, mode='a')

# Additional Requests
for i in range(10):
    for subreddit in subreddits:
        # Look up last anchor
        transactions_df = pd.read_csv('./data/'+subreddit+'_transaction_log.csv')
        anchor = transactions_df['anchor'][0]
    
        # Modify request parameters to get next 100 per request
        params = {'limit': 100, 'after': anchor}
        
        # Make new response
        res = requests.get(base_url+subreddit, headers=headers, 
                           params=params)
        
        # Loop through to gather all info
        #anchor = res.json()['data']['after']
        postings = []
        for i in range(len(res.json()['data']['children'])):
            posting = []
            posting.append(time.ctime())
            posting.append((res.json()['data']['children'][i]['data']['name']))
            posting.append((res.json()['data']['children'][i]['data']['title']))
            posting.append((time.ctime(res.json()['data']['children'][i]
                                       ['data']['created_utc'])))
            posting.append((res.json()['data']['after']))
            posting.append(subreddit)
            postings.append(posting)
        
            pull = pd.DataFrame(postings, 
                            columns=['time_pulled', 'fullname', 'titles',
                                      'times_created', 'anchors', 'subreddit'])
            pull['times_created'] = pd.to_datetime(pull['times_created'])
            pull.sort_values(by=['times_created'], inplace=True, ascending=False)
        
        # Update Transaction log
        t_log = pd.read_csv('./data/' + subreddit + '_transaction_log.csv')
        transactions = []
        new_total = (len(pull) + t_log.iloc[-1 , 2])
        new_anchor = res.json()['data']['after']
        transaction = [subreddit, len(pull), new_total, time.ctime(), 
                       new_anchor]
        transactions.append(transaction)
        transactions = pd.DataFrame(transactions, 
                                    columns=['subreddit', 'pulled_postings', 
                                             'total_postings', 'times_created', 
                                             'anchor'])

        # Write to csv file
        pull.to_csv('./data/' + subreddit + '_pulls.csv', mode='a', 
                    header=False, index=False)
        transactions.to_csv('./data/' + subreddit + '_transaction_log.csv', 
                            mode='a', header=False, index=False)

        # Clean duplicates
        cleaning_df = pd.read_csv('./data/' + subreddit + '_pulls.csv')
        cleaning_df.drop_duplicates(subset=['fullname'], keep='first', inplace=True)
        cleaning_df.to_csv('./data/' + subreddit +'_pulls.csv', index=False)

# Additional requests

subreddits = [subreddit_1, subreddit_2]
for i in range(howlong):
    for subreddit in subreddits:
     
        # Look up last anchor
        transactions_df = pd.read_csv('./data/'+subreddit+'_transaction_log.csv')
        anchor = transactions_df['anchor'][0]
    
        # Modify request parameters to get next 100 per request
        params = {'limit': 100, 'after': anchor}
        
        # Make new response
        new_res = requests.get(base_url+subreddit, headers=headers, params=params)
        
        # Loop through to gather all info
        #anchor = res.json()['data']['after']
        postings = []
        for i in range(len(new_res.json()['data']['children'])):
            posting = []
            posting.append(time.ctime())
            posting.append((new_res.json()['data']['children'][i]['data']['name']))
            posting.append((new_res.json()['data']['children'][i]['data']['title']))
            posting.append((time.ctime(new_res.json()['data']['children'][i]['data']['created_utc'])))
            posting.append((new_res.json()['data']['after']))
            posting.append(subreddit)
            postings.append(posting)
        
            pull = pd.DataFrame(postings, 
                            columns=['time_pulled', 'fullname', 'titles', 'times_created', 
                                     'anchors', 'subreddit'])
            pull['times_created'] = pd.to_datetime(pull['times_created'])
            pull.sort_values(by=['times_created'], inplace=True, ascending=False)
        
        # Update Transaction log
        t_log = pd.read_csv('./data/' + subreddit + '_transaction_log.csv')
        transactions = []
        new_total = (len(pull) + t_log.iloc[-1 , 2])
        new_anchor = new_res.json()['data']['after']
        transaction = [subreddit, len(pull), new_total, time.ctime(), new_anchor]
        transactions.append(transaction)
        transactions = pd.DataFrame(transactions, 
                                    columns=['subreddit', 'pulled_postings', 
                                             'total_postings', 'times_created', 'anchor'])
    
        # Write to csv file
        pull.to_csv('./data/' + subreddit + '_pulls.csv', mode='a', header=False, index=False)
        transactions.to_csv('./data/' + subreddit + '_transaction_log.csv', 
                            mode='a', header=False, index=False)
    
        # Clean duplicates
        cleaning_df = pd.read_csv('./data/' + subreddit + '_pulls.csv')
        cleaning_df.drop_duplicates(subset=['fullname'], keep='first', inplace=True)
        cleaning_df.to_csv('./data/' + subreddit +'_pulls.csv', index=False)
        
        time.sleep(2)


print('Thank you for your patience.  Your posts are saved.')