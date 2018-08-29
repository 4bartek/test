from django.shortcuts import render
from . import views
from rss_reader.views import rss_reader


import json
import requests as r
# Create your views here.

def rss_reader():

    import feedparser
    import re
    from dateutil.parser import parse
    from time import mktime
    from datetime import datetime

    feed_s = []
    url = ['https://bithub.pl/feed/','https://cyfrowaekonomia.pl/feed/','http://bitcoin.pl/?format=feed&type=rss']

    for ur in url:
        
        f = feedparser.parse(ur)

        for e in f['entries']:
            print(ur)

            if ur == 'https://bithub.pl/feed/':
                img = ((((e.get('summary', '')).split('src="'))[1]).split('"'))[0]
                description = ((e.get('summary', '')).split('<p>'))[1]

            elif ur == 'http://bitcoin.pl/?format=feed&type=rss':
                summary = e.get('summary', '')
                description = (((summary.split('</span></p>'))[-2]).split('" />'))[-1]
                description = description.replace('<br />','')
                description = description.replace('</span>','')
                description = description.replace('<span style="font-size: 12pt;">','')
                img = ((((e.get('summary', '')).split('src="'))[1]).split('"'))[0]
                date = e.published_parsed

            elif ur == 'https://cyfrowaekonomia.pl/feed/':
                description = e.get('summary', '')
                img = ''
            
            description = description.replace('[&#8230;]','...')
            description = description.replace('</p>','')
            description = description.replace('&#8211;','-')

            

            source = (ur.split('/'))[2]

            title = e.get('title', '')
            link = e.get('link', '')

            pub = e['published_parsed']
            published = datetime.fromtimestamp(mktime(pub))
            
            pub_sorter = published.strftime('%Y%m%d')
            published = published.strftime('%d-%m-%Y')

            feed = {
                'title':title,
                'link':link,
                'description':description,
                'img':img,
                'published': published,
                'pub_sorter': pub_sorter,
                'source': source,
            }

            feed_s.append(feed)

    feed_s.sort(key=lambda item:item['pub_sorter'], reverse=True)

    return feed_s

def getToken(id, secret):
    import json
    # Get the id and secret from https://api.coinmarketcal.com/developer/register
    payload = {'grant_type': 'client_credentials', 'client_id': id, 'client_secret': secret}
    url = "https://api.coinmarketcal.com/oauth/v2/token"
    try:
        events = r.post(url, data=payload)
        result = json.loads(events.text)
    except json.decoder.JSONDecodeError:
        print("JSONDecodeError")
        result = []
    return result


def getEvents(token, page=None, max=None, dateRangeStart=None, dateRangeEnd=None,
              coins=None, categories=None, sortBy=None, showOnly=None,):
    
    payload = {
            "page": page,
            "max": max,
            "dateRangeStart": dateRangeStart,
            "dateRangeEnd": dateRangeEnd,
            "coins": coins,
            "categories": categories,
            "sortBy": sortBy,
            "showOnly": showOnly,
            'access_token': token,
             }

    url = "https://api.coinmarketcal.com/v1/events"
    try:
        events = r.get(url, params=payload)
        coinmarketcal_events = json.loads(events.text)
    except json.decoder.JSONDecodeError:
        print("JSONDecodeError")
        coinmarketcal_events = ['fetch error']
    
    return coinmarketcal_events

def info(request):

    import requests
    import json

    # coinmarketcall events
    token = (getToken('906_3e8w8a4nox6ogk0gs8c4k88wsk4o4g4w80c0k8040wcg0csc0k', '6cz6n3bwr2o84g0g04ws8o80coc08cgoss4s4koksw0s4ocg00'))['access_token']
    coinmarketcal_events = getEvents(token, page=None, max=None, dateRangeStart=None, dateRangeEnd=None,
              coins=None, categories=None, sortBy=None, showOnly=None,)
    #


    rss_feeds = rss_reader()
    ico_req = requests.get("https://api.icowatchlist.com/public/v1/all")
    ico_req = json.loads(ico_req.content)
    
    ico_live = ico_req['ico']['live']
    ico_upcoming = ico_req['ico']['upcoming']
    ico_finished = ico_req['ico']['finished']
    

    return render(request, 'info.html', {
        'ico_live':ico_live, 
        'ico_upcoming':ico_upcoming,
        'ico_finished': ico_finished,
        'rss_feeds': rss_feeds,
        'coinmarketcal_events': coinmarketcal_events,
        })

