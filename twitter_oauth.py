import requests
from twitter import *

with open('key/token','r') as f:
    token=f.readlines()
    CK = token[0].replace('\n','')  # Consumer Key
    CS = token[1].replace('\n','')  # Consumer Secret
    AT = token[2].replace('\n','')  # Access Token
    AS = token[3].replace('\n','')  # Accesss Token Secert

auth = OAuth(CK,CS,AT,AS)

#自分のタイムラインのツイートおよびユーザーの情報が流れる
twitter_stream = TwitterStream(auth=auth, domain='userstream.twitter.com')

for tweet in twitter_stream.user():
    print(tweet)
