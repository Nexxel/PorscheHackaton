"""
Definition of views.
"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .models import *
import requests
import json

from .connect import (searchHashtag, getMetaTweet, giveLike, takeOffLike,
                     giveRetweet, takeOffRetweet, giveFollow, takeOffFollow,
                     getAreaInfluencer)
from .forms import (SearchFormFitnes, SearchFormFood, SearchFormTech,
                    SearchFormTravel, SearchFormFashion, SearchFormInfluencer)

from .tags import (_hashtags_fitness, _hashtags_food, _hashtags_travel,
                  _hashtags_tech, _hashtags_fashion, _hashtags_Influencer)

hashtagsInsta = {'_hashtags_fitness': {'gethealthy': 1, 'healthylife': 2, 'healthtalk': 3, 'eatclean': 4, 'fitfood': 5, 'nutrition': 6, 'fitquote': 7, 'fitnessmotivation': 8, 'fitspo': 9, 'getfit': 10, 'fitfam': 11, 'trainhard': 12, 'noexcuses': 13, 'fitnessaddict': 14, 'gymlife': 15, 'girlswholift': 16, 'workout': 17, 'fitlife': 18, 'sweat': 20}, '_hashtags_food': {'foodie': 21, 'foodporn': 22, 'foodgasm': 23, 'nom': 24, 'food': 5, 'pizza': 26, 'foodstagram': 28, 'menwhocook': 29, 'sushi': 30, 'yummy': 31, 'foodcoma': 32, 'eathealthy': 33, 'instafood': 34, 'delicious': 35, 'foodpic': 36, 'cooking': 37, 'snack': 38, 'tasty': 39, 'cleaneating': 40}, '_hashtags_travel': {'travel': 41, 'instatravel': 42, 'travelgram': 43, 'tourist': 44, 'tourism': 45, 'vacation': 46, 'traveling': 47, 'travelblogger': 48, 'wanderlust': 49, 'ilovetravel': 50, 'instavacation': 51, 'traveldeeper': 52, 'getaway': 53, 'wanderer': 54, 'adventure': 55, 'travelphotography': 56, 'roadtrip': 57, 'mytravelgram': 58, 'igtravel': 59, 'traveler': 60}, '_hashtags_tech': {'technology': 61, 'science': 62, 'bigdata': 63, 'iphone': 64, 'ios': 65, 'android': 66, 'mobile': 67, 'video': 68, 'design': 69, 'innovation': 70, 'startups': 71, 'tech': 72, 'cloud': 73, 'gadget': 74, 'instatech': 75, 'electronic': 76, 'device': 77, 'techtrends': 78, 'technews': 79, 'engineering': 80}, '_hashtags_fashion': {'fashion': 81, 'fashionista': 82, 'fashionblogger': 83, 'ootd': 84, 'style': 85, 'stylish': 86, 'streetstyle': 87, 'streetwear': 88, 'fashioninspo': 89, 'trend': 90, 'styleoftheday': 91, 'stylegram': 92, 'mensfashion': 93, 'lookbook': 94, 'todayiwore': 95, 'beauty': 96, 'makeupaddict': 97, 'hair': 98, 'instafashion': 99, 'vintage': 100}}
hashtagsInstaWithoutBranch = {'gethealthy': 1, 'healthylife': 2, 'healthtalk': 3, 'eatclean': 4, 'fitfood': 5, 'nutrition': 6, 'fitquote': 7, 'fitnessmotivation': 8, 'fitspo': 9, 'getfit': 10, 'fitfam': 11, 'trainhard': 12, 'noexcuses': 13, 'fitnessaddict': 14, 'gymlife': 15, 'girlswholift': 16, 'workout': 17, 'fitlife': 18, 'sweat': 20, 'foodie': 21, 'foodporn': 22, 'foodgasm': 23, 'nom': 24, 'food': 5, 'pizza': 26, 'foodstagram': 28, 'menwhocook': 29, 'sushi': 30, 'yummy': 31, 'foodcoma': 32, 'eathealthy': 33, 'instafood': 34, 'delicious': 35, 'foodpic': 36, 'cooking': 37, 'snack': 38, 'tasty': 39, 'cleaneating': 40, 'travel': 41, 'instatravel': 42, 'travelgram': 43, 'tourist': 44, 'tourism': 45, 'vacation': 46, 'traveling': 47, 'travelblogger': 48, 'wanderlust': 49, 'ilovetravel': 50, 'instavacation': 51, 'traveldeeper': 52, 'getaway': 53, 'wanderer': 54, 'adventure': 55, 'travelphotography': 56, 'roadtrip': 57, 'mytravelgram': 58, 'igtravel': 59, 'traveler': 60, 'technology': 61, 'science': 62, 'bigdata': 63, 'iphone': 64, 'ios': 65, 'android': 66, 'mobile': 67, 'video': 68, 'design': 69, 'innovation': 70, 'startups': 71, 'tech': 72, 'cloud': 73, 'gadget': 74, 'instatech': 75, 'electronic': 76, 'device': 77, 'techtrends': 78, 'technews': 79, 'engineering': 80, 'fashion': 81, 'fashionista': 82, 'fashionblogger': 83, 'ootd': 84, 'style': 85, 'stylish': 86, 'streetstyle': 87, 'streetwear': 88, 'fashioninspo': 89, 'trend': 90, 'styleoftheday': 91, 'stylegram': 92, 'mensfashion': 93, 'lookbook': 94, 'todayiwore': 95, 'beauty': 96, 'makeupaddict': 97, 'hair': 98, 'instafashion': 99, 'vintage': 100}

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    option = request.POST.get('option')
    influencers = list()
    if option:
        influencers = process_selection(option)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'option':option,
            'influencers':influencers
        }
    )

def process_selection(selection):
    hashtags_list = get_hashtags_list(selection)
    user_ids_list = get_user_ids(hashtags_list)
    influencers_data = get_influencers_data(user_ids_list)
    return influencers_data
    
          
def get_dictionary(selection):
    if (selection == "Fitness"):
        return '_hashtags_fitness'
    if (selection == "Food"):
        return '_hashtags_food'
    if (selection == "Travel"):
        return '_hashtags_travel'
    if (selection == "Tech"):
        return '_hashtags_tech'
    if (selection == "Fashion"):
        return '_hashtags_fashion'

def get_hashtags_list(selection, min_posts=430):
    hashtags_list = list()
    for item, n in hashtagsInsta[get_dictionary(selection)].items():
        r = requests.get('http://Hackathon.ocupa2.com/instagram/{}/top_media?'.format(n),data='{user_id:17481}')
        posts = r.json()
        for key in posts.keys():
            if (len(posts[key]) > min_posts):
                hashtags_list.append(posts[key])
    return hashtags_list

def get_user_ids(hashtags_list, min_likes=2, min_coments=1):
    user_ids_list = list()
    for hashtag_posts in hashtags_list:
        for post in hashtag_posts:
            if post['likeCount'] > min_likes and post['commentsCount'] > min_coments:
                r = requests.get('http://Hackathon.ocupa2.com/instagram/media/{}?{}'.format(post['id'],'fields=username'))
                users = r.json()
                for user in users:
                    for key, value in user.items():
                        user_ids_list.append(value)
    return set(user_ids_list)

def get_influencers_data(user_ids_list, min_ratio=0.125):
    influencers_data = list()
    for user_id in user_ids_list:
        r = requests.get('http://Hackathon.ocupa2.com/instagram/{}?{}'.format(user_id, 'fields=id,follower_count,media_count,username'))
        influencers = r.json()
        for influencer in influencers:
            influencer['average'] = round(influencer['followerCount']/influencer['mediaCount'],3)
            if influencer['average'] > min_ratio:
                influencers_data.append(influencer)
    influencers_data = sorted(influencers_data, key=lambda k: k['average'], reverse=True)
    return influencers_data

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/users.html',
        {
            'title':'users',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def users(request):
    """Renders the users page."""
    assert isinstance(request, HttpRequest)
    option = request.POST.get('option')
    users = list()
    if option:
        users = get_users(option)
    return render(
        request,
        'app/users.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'hashtags_fitness':HastagFitness.THEME_CHOICES,
            'hashtags_food':HastagFood.THEME_CHOICES,
            'hashtags_travel':HastagTravel.THEME_CHOICES,
            'hashtags_tech':HastagTech.THEME_CHOICES,
            'hashtags_fashion':HastagFashion.THEME_CHOICES,
            'option':option,
            'users':users
        }
    )

def posts(request):
    """Renders the users page."""
    pages = list()
    assert isinstance(request, HttpRequest)
    option = request.POST.get('option')
    
    posts = list()
    likeup = request.POST.get('likes')
    if likeup:
       r = requests.get('http://Hackathon.ocupa2.com/instagram/media/{}/like?user_id=17481&action=like'.format(likeup))
    if option:
        posts = get_posts_by_hashtag(option)
        for value in posts:
            pages.append( postObject( value['id'],value['likeCount'] ) )
    else:
        posts = get_posts_by_hashtag('food')
        for value in posts:
            pages.append( postObject( value['id'],value['likeCount'] ) )


    paginator = Paginator(pages, 15) # 3 posts in each page
    page = request.GET.get('page',1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages) 


    return render(
        request,
        'app/posts.html',
        {
            'title':'Post Page',
            'year':datetime.now().year,
            'hashtags_fitness':HastagFitness.THEME_CHOICES,
            'hashtags_food':HastagFood.THEME_CHOICES,
            'hashtags_travel':HastagTravel.THEME_CHOICES,
            'hashtags_tech':HastagTech.THEME_CHOICES,
            'hashtags_fashion':HastagFashion.THEME_CHOICES,
            'option':option,
            'posts':posts
        }
    )

def get_posts_by_hashtag(selection):
    hashtags_list = list()
    id = hashtagsInstaWithoutBranch[selection]
    r = requests.get('http://Hackathon.ocupa2.com/instagram/{}/recent_media?'.format(id),data='{user_id:17481}')
    posts = r.json()
    for item in posts['data']:
        element = {'id':item['id'], 'likeCount':item['likeCount']}
        hashtags_list.append(element)
    return hashtags_list

def get_users(selection):
    hashtags_list = get_posts_by_hashtag(selection)
    user_ids_list = get_user_ids_by_hashtag(hashtags_list)
    users_data = get_users_data(user_ids_list)
    return users_data

def get_user_ids_by_hashtag(hashtags_list):
    user_ids_list = list()
    for post in hashtags_list:
        r = requests.get('http://Hackathon.ocupa2.com/instagram/media/{}?{}'.format(post['id'],'fields=username'))
        users = r.json()
        for user in users:
            for key, value in user.items():
                user_ids_list.append(value)
    return set(user_ids_list)

def get_users_data(user_ids_list):
    users_data = list()
    for user_id in user_ids_list:
        r = requests.get('http://Hackathon.ocupa2.com/instagram/{}?{}'.format(user_id, 'fields=id,follower_count,username'))
        users = r.json()
        for user in users:
            users_data.append(user)
    users_data = sorted(users_data, key=lambda k: k['followerCount'], reverse=True)
    return users_data

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'This is our application for making the analise for Porsche',
            'year':datetime.now().year,
        }
    )

def tweets(request):
    form_Influencer = SearchFormInfluencer()
    data = get_method(request)
    ctx = {'data': data, 'form_Influencer':form_Influencer,
           'hashtags_fitness': _hashtags_fitness,
           'hashtags_food': _hashtags_food,
           'hashtags_travel': _hashtags_travel,
           'hashtags_tech': _hashtags_tech,
           'hashtags_fashion': _hashtags_fashion}
    return render(request, 'app/tweets.html', ctx)

def users_tweet(request):
    form_Influencer = SearchFormInfluencer()
    data = get_method(request)
    ctx = {'data': data, 'form_Influencer':form_Influencer,
           'hashtags_fitness': _hashtags_fitness,
           'hashtags_food': _hashtags_food,
           'hashtags_travel': _hashtags_travel,
           'hashtags_tech': _hashtags_tech,
           'hashtags_fashion': _hashtags_fashion}
    return render(request, 'app/users_tweet.html', ctx)

def get_method(request):
    data = ''
    if 'option' in request.GET:
        data = searchHashtag(request.GET['option'])
    elif 'area_influencer' in request.GET:
        data = getAreaInfluencer(request.GET['area_influencer'])
    return data

def like_view(request, pk):
    if request.method == 'GET':
        data = giveLike(pk)
        print(data)
        if data['status'] == 200:
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'ko'})
    else:
        return HttpResponseNotFound('Invalid 404')

def dislike_view(request, pk):
    if request.method == 'GET':
        data = takeOffLike(pk)
        if data['status'] == 200:
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'ko'})
    else:
        return HttpResponseNotFound('Invalid 404')

def giveRetweet_view(request, pk):
    if request.method == 'GET':
        data = giveRetweet(pk)
        if data['status'] == 200:
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'ko'})
    else:
        return HttpResponseNotFound('Invalid 404')

def takeOffRetweet_view(request, pk):
    if request.method == 'GET':
        data = takeOffRetweet(pk)
        if data['status'] == 200:
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'ko'})
    else:
        return HttpResponseNotFound('Invalid 404')

def giveFollow_view(request, pk):
    if request.method == 'GET':
        data = giveFollow(pk)
        if data['status'] == 200:
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'ko'})
    else:
        return HttpResponseNotFound('Invalid 404')

def takeOffFollow_view(request, pk):
    if request.method == 'GET':
        data = takeOffFollow(pk)
        if data['status'] == 200:
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'ko'})
    else:
        return HttpResponseNotFound('Invalid 404')



class postObject(object):
    id_user = ''
    likeCount = ''
    def __init__(self,id_user,likes):
     self.id_user = id_user
     self.likeCount = likes  


