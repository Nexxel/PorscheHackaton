"""
Definition of models.
"""

from django.db import models

# Create your models here.   

class HastagFitness(models.Model):

    THEME_CHOICES = (
        ('gethealthy','gethealthy'),
        ( 'healthylife','healthylife'),
        ( 'healthtalk','healthtalk'),
        ("eatclean","eatclean"),
        ("fitfood","fitfood"),
        ("nutrition","nutrition"),
        ("fitquote","fitquote"),
        ("fitnessmotivation","fitnessmotivation"),
        ("fitspo","fitspo"),
        ("getfit","getfit"),
        ("fitfam","fitfam"),
        ("trainhard","trainhard"),
        ("noexcuses","noexcuses"),
        ("fitnessaddict","fitnessaddict"),
        ("gymlife","gymlife"),
        ("girlswholift","girlswholift"),
        ("workout","workout"),
        ("fitlife","fitlife"),
        ("gymlife","gymlife"),
        ("sweat","sweat"),
        )
    
    name = models.CharField(max_length=20,choices=THEME_CHOICES, unique=True)

    def str(self):
        return self.name
   

class HastagFood(models.Model):

    THEME_CHOICES = (
        ('foodie','foodie'),          
        ('foodporn','foodporn'),
        ('foodgasm','foodgasm'),
        ("nom","nom"),
        ("food","food"),
        ("pizza","pizza"),
        ("foodporn","foodporn"),
        ("foodstagram","foodstagram"),
        ("menwhocook","menwhocook"),
        ("sushi","sushi"),
        ("yummy","yummy"),
        ("foodcoma","foodcoma"),
        ("eathealthy","eathealthy"),
        ("instafood","instafood"),
        ("delicious","delicious"),
        ("foodpic","foodpic"),
        ("cooking","cooking"),
        ("snack","snack"),
        ("tasty","tasty"),
        ("cleaneating","cleaneating"),
        )
    
    name = models.CharField(max_length=20,choices=THEME_CHOICES, unique=True)

    def str(self):
        return self.name
   

class HastagTravel(models.Model):

    THEME_CHOICES = (
        ('travel','travel'),
        ('instatravel','instatravel'),
        ('travelgram','travelgram'),
        ("tourist","tourist"),
        ("tourism","tourism"),
        ("vacation","vacation"),
        ("traveling","traveling"),
        ("travelblogger","travelblogger"),
        ("wanderlust","wanderlust"),
        ("ilovetravel","ilovetravel"),
        ("instavacation","instavacation"),
        ("traveldeeper","traveldeeper"),
        ("getaway","getaway"),
        ("wanderer","wanderer"),
        ("adventure","adventure"),
        ("travelphotography","travelphotography"),
        ("roadtrip","roadtrip"),
        ("snamytravelgram","snamytravelgram"),
        ("igtravel","igtravel"),
        ("traveler","traveler"),
        )
    
    name = models.CharField(max_length=20,choices=THEME_CHOICES, unique=True)

    def str(self):
        return self.name
   

class HastagTech(models.Model):

    THEME_CHOICES = (
        ('travtechnologyel','travtechnologyel'),         
        ('science','science'),
        ('bigdata','bigdata'),
        ("iphone","iphone"),
        ("ios","ios"),
        ("android","android"),
        ("mobile","mobile"),
        ("video","video"),
        ("design","design"),
        ("innovation","innovation"),
        ("startups","startups"),
        ("tech","tech"),
        ("cloud","cloud"),
        ("gadget","gadget"),
        ("instatech","instatech"),
        ("electronic","electronic"),
        ("device","device"),
        ("techtrends","techtrends"),
        ("technews","technews"),
        ("engineering","engineering"),
        )
    
    name = models.CharField(max_length=20,choices=THEME_CHOICES, unique=True)

    def str(self):
        return self.name
   


class HastagFashion(models.Model):


    THEME_CHOICES = (
        ('fashion','fashion'),
        ('fashionista','fashionista'),
        ('fashionblogger','fashionblogger'),
        ("ootd","ootd"),
        ("style","style"),
        ("stylish","stylish"),
        ("streetstyle","streetstyle"),
        ("fashioninspo","fashioninspo"),
        ("trend","trend"),
        ("styleoftheday","styleoftheday"),
        ("stylegram","stylegram"),
        ("mensfashion","mensfashion"),
        ("lookbook","lookbook"),
        ("todayiwore","todayiwore"),
        ("beauty","beauty"),
        ("makeupaddict","makeupaddict"),
        ("hair","hair"),
        ("instafashion","instafashion"),
        ("vintage","vintage"),
        ("engineering","engineering"),
        )
    
    name = models.CharField(max_length=20,choices=THEME_CHOICES, unique=True)

    def str(self):
        return self.name