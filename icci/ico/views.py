from django.shortcuts import render

# Create your views here.

def ico_fetch():

    import requests
    import json

    ico_req = requests.get("https://api.icowatchlist.com/public/v1/all")
    ico_req = json.loads(ico_req.content)
    
    ico_live = ico_req['ico']['live']
    ico_upcoming = ico_req['ico']['upcoming']
    ico_finished = ico_req['ico']['finished']
    
    return {
        'ico_live':ico_live,
        'ico_upcoming':ico_upcoming,
        'ico_finished':ico_finished}

def ico(request):

    ico_live,ico_upcoming,ico_finished = ico_fetch()

    return render(request, 'templates/ico.html', {
        'ico_live':ico_live, 
        'ico_upcoming':ico_upcoming,
        'ico_finished': ico_finished,
        })
    
