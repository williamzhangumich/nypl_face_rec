import requests
import string
from bs4 import BeautifulSoup
import urllib
import re
import os

def get_pbv_ref():
    for i in range(20000):
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

def get_people_by_show(show_id):
    """
    Based on show_id (see ref.txt), return a collecition of people name and id
    Grouped by 'Cast', 'Music Credits', 'Production Credits'
    Person id could be used to retrieve headshots
    """
    
    url = "http://www.playbillvault.com/Show/Detail/Cast/%d"%show_id
    r = requests.get(url)
    soup = BeautifulSoup(r.text) 
    
    # Should be 3 groups of people: cast, music credits, production credits
    groups = soup.findAll('div', { "class" : "showcast" })
    people_id_collection = {}
    for group in groups:
        group_type = str(group.find('h3').string.split(':')[-1][15:])
        people_objs = group.findAll('div',{ "class" : "image" })
        person_id = []
        for person in people_objs:
            anchor = person.find('a')
            if anchor: # img block not empty
                # href: /Person/Detail/id/name
                id, name = anchor.get('href').split('/')[3:5]
                id = int(id)
                name = name.replace('+','_').replace('-','_')
                person_id.append((id, name))
        people_id_collection[group_type] = person_id
    
    # keys: 'Cast', 'Music Credits', 'Production Credits'
    # values: [(id, person), (.., ..), ....]
    return people_id_collection

def retrieve_headshot(person_id, folder_path='./'):
    """
    Given person_id, download all his/her headshots on Playbill Vault 
    to the target folder
    """
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    url = "http://www.playbillvault.com/Person/Detail/Headshots/%d"%person_id
    r = requests.get(url)
    soup = BeautifulSoup(r.text) 
    img_urls = [s.get('src') for s in soup.findAll('img') if re.search(r'thumbs/h75', s.get('src'))]
    
    name =  soup.findAll('div',{ "class" : "breadcrumb" })[0].find('a').string.strip('<').replace(' ','')
    print "Got images for: ", name
    
    index = 1
    for url in img_urls:
        url = 'http://www.playbillvault.com'+url.replace('thumbs/h75/', '')
        print url
        urllib.urlretrieve(url, folder_path+'/'+name+'_%d.jpg'%index)
        index+=1
    

if __name__ == "__main__":
    
    # Get the people in show 11020 (Wicked)
    # keys: 'Cast', 'Music Credits', 'Production Credits'
    # values: [(id, person), (.., ..), ....]
    people_id = get_people_by_show(11020)
    
    # We print all cast (include replacements)
    for id, name in people_id['Cast']:
        print id, name
    
    # Get first person 54551 (Idina_Menzel)
    person = people_id['Cast'][0]
    
    # Get headshots with id 54551
    retrieve_headshot(person[0], 'Idina_Menzel')
      
