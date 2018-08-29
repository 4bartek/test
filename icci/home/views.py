from django.shortcuts import render
from ico.views import ico_fetch
from info.views import rss_reader, getToken, getEvents 


# Create your views here.

def home(request):

    #ico
    ico = ico_fetch()
    ico_live = ico['ico_live']

    #artykuły
    feeds = rss_reader()
    home_feeds = []
    for x in feeds:
        if len(home_feeds) < 100:
            #if x['img'] != '':
            home_feeds.append(x)

    #wydarzenia
    token = (getToken('906_3e8w8a4nox6ogk0gs8c4k88wsk4o4g4w80c0k8040wcg0csc0k', '6cz6n3bwr2o84g0g04ws8o80coc08cgoss4s4koksw0s4ocg00'))['access_token']
    coinmarketcal_events = getEvents(token, page=None, max=None, dateRangeStart=None, dateRangeEnd=None,
              coins=None, categories=None, sortBy=None, showOnly=None,)



    return render(request, 'home.html', {
        'ico_live':ico_live[0:100], 'feeds':home_feeds, 'events':coinmarketcal_events[0:100],
        })
