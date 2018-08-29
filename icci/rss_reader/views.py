from django.shortcuts import render

# Create your views here.



def rss_fetch():

    import feedparser
    import re

    ### BITCOIN.PL ###


    #'https://cryptonews.pl/feed/',

    rss_feeds = []
    #url = 'https://bithub.pl/feed/'
    url = [ 'https://cyfrowaekonomia.pl/feed/','http://bitcoin.pl/?format=feed&type=rss',]
    
    for url in url:
        try:
            feeds = feedparser.parse(url)
            
            for x in (feeds['entries']):
                print(x)
                summary = (x['summary'])
                
                img = summary.replace('<p style="text-align: justify;"><span style="font-size: 12pt;"><img style="margin-right: 15px; margin-bottom: 15px; margin-left: 15px; float: left;" src="','')
                img = img.replace('<p style="text-align: justify;"><span style="font-size: 12pt;"><img style="margin-right: 15px; margin-bottom: 15px; margin-left: 15px; float: left;" src=','')
                #img = (re.sub('^.*?width="285" height="160" />', '', img))

                img = (img.split('.jpg"'))[0]+'.jpg'

                if img[0:3] != 'htt':
                    img = False

                source = url.split('/')[2]
                summary_clean = (re.sub('^.*?width="285" height="160" />', '', summary))
                summary_clean = summary_clean.replace('</span></p>','')
                summary_clean = summary_clean.replace('<br />','')
                summary_clean = summary_clean.replace('<span style="font-size: 12pt;">','')
                summary_clean = summary_clean.replace('</span>','')
                summary_clean = summary_clean.replace('&nbsp;','')
                summary_clean = summary_clean[0:10]

                rss_feed = {
                    'title':x['title'], 
                    'img': img,
                    'description':summary_clean,
                    'source': source,
                    'published': x['published'],
                    'link': (x['links'])[0]['href'],
                }

                rss_feeds.append(rss_feed)
        except:
            rss_feeds = [{'title': 'błąd except'},{'title': 'błąd except1'}]

    
    
    ### ###
    rss_feeds.sort(key=lambda item:item['published'], reverse=True)
    return rss_feeds

def rss_reader(request):
    
    return render(request, 'rss_reader.html', {'rss_feeds':rss_fetch()})
