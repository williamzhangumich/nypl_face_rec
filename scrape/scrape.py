import requests
import string
from bs4 import BeautifulSoup

for i in range(8460,20000):
    url = "http://www.playbillvault.com/Show/Detail/%d"%i
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    title = soup.findAll('h2')[1].string
    #import ipdb; ipdb.set_trace()
    if title:
        print i, title.encode('utf-8')
        with open('ref.txt','a') as h:
            h.write("%d\t%s\n"%(i,title.encode('UTF-8')))
    else:
        print "%d is not found"%i
"""

params = {'artist':artist,'limit':999999,'format':'json',
        'api_key':api_will}
#try connection and log timeouts
try:
    print "\t-%s:\tDownloading from API"%artist
    r = requests.get(url,params=params,timeout=5)
    print "\t-%s:\tDownload complete"%artist
except Exception,e:
    print 'API QUERY ERROR for artist :%s:%s\n'%(artist,e)
    log_error('API QUERY ERROR for artist :%s:%s\n'%(artist,e))
    return
#get json string handle respons (insert db)
json_string = filt(r.text)
"""