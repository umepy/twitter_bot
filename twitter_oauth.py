#coding:utf-8

from requests_oauthlib import OAuth1
import requests
import pprint
import json

with open('key/token','r') as f:
    token=f.readlines()
    CK = token[0].replace('\n','')  # Consumer Key
    CS = token[1].replace('\n','')  # Consumer Secret
    AT = token[2].replace('\n','')  # Access Token
    AS = token[3].replace('\n','')  # Accesss Token Secert
url = "https://userstream.twitter.com/1.1/user.json"

auth = OAuth1(CK,CS,AT,AS)
r = requests.post(url,auth=auth,stream=True)

for line in r.iter_lines():
    pprint.pprint(json.load(line.decode('utf-8')))