import requests
from .tags import (_hashtags_fitness, _hashtags_food, _hashtags_travel,
                  _hashtags_tech, _hashtags_fashion, _hashtags_Influencer)

def searchHashtag(tag):
    url = 'http://Hackathon.ocupa2.com/twitter/1.1/search/tweets.json?q='+tag
    data = requests.get(url, timeout=1.5)
    return data.json()

def getMetaTweet(TweetId):
    url = 'http://Hackathon.ocupa2.com/twitter/1.1/statuses/retweets/'+str(TweetId)+'.json'
    data = requests.get(url, timeout=1.5)
    return data.json()

def giveLike(TweetId):
    url = 'http://hackathon.ocupa2.com/twitter/1.1/favorites/create.json?id='+str(TweetId)+'&bearer=4biO375qjLawxAqVbXBU'
    data = requests.get(url, timeout=1.5)
    return data.json()

def takeOffLike(TweetId):
    url = 'http://hackathon.ocupa2.com/twitter/1.1/favorites/destroy.json?id='+str(TweetId)+'&bearer=4biO375qjLawxAqVbXBU'
    data = requests.get(url, timeout=1.5)
    return data.json()

def giveRetweet(TweetId):
    url = 'http://hackathon.ocupa2.com/twitter/1.1/statuses/retweet/'+str(TweetId)+'.json?bearer=4biO375qjLawxAqVbXBU'
    data = requests.get(url, timeout=1.5)
    return data.json()

def takeOffRetweet(TweetId):
    url = 'http://hackathon.ocupa2.com/twitter/1.1/statuses/unretweet/'+str(TweetId)+'.json?bearer=4biO375qjLawxAqVbXBU'
    data = requests.get(url, timeout=1.5)
    return data.json()

def giveFollow(userId):
    url = 'http://hackathon.ocupa2.com/twitter/1.1/friendships/create.json?user_id='+str(userId)+'&bearer=4biO375qjLawxAqVbXBU'
    data = requests.get(url, timeout=1.5)
    return data.json()

def takeOffFollow(userId):
    url = 'http://hackathon.ocupa2.com/twitter/1.1/friendships/destroy.json?user_id='+str(userId)+'&bearer=4biO375qjLawxAqVbXBU'
    data = requests.get(url, timeout=1.5)
    return data.json()

def getAreaInfluencer(area):
    datos = []
    area = '_hashtags_'+area
    area = eval(area)
    for x in range(len(area)):
        url = 'http://Hackathon.ocupa2.com/twitter/1.1/search/tweets.json?q='+area[x][0]
        data = requests.get(url, timeout=1.5)
        datos += data.json()
    return datos
