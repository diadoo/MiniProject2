import sys
import re
import pymongo
import json
import time
import datetime
import requests
from bs4 import BeautifulSoup

dbname = "fdac18mp2" #please use this database
collname = "glprj_jpovlin" #please modify so you store data in your collection
my_char = 'f'

# beginning page index
begin = "1"
client = pymongo.MongoClient()

db = client[dbname]
coll = db[collname]


gitlab_url = "https://gitlab.com/api/v4/projects?archived=false&membership=false&order_by=created_at&owned=false&page=" + begin + \
    "&per_page=99&simple=false&sort=desc&starred=false&statistics=false&with_custom_attributes=false&with_issues_enabled=false&with_merge_requests_enabled=false"

gleft = 20

source_url = "https://sourceforge.net/directory/?q=" + my_char + "&sort=name&page="
rest_url = "https://sourceforge.net/rest/p/"

header = {'per_page': 99}

# check remaining query chances for rate-limit restriction
def wait(left):
    global header
    while (left < 20):
        l = requests.get('https://gitlab.com/api/v4/projects', headers=header)
        if (l.ok):
            left = int(l.headers.get('RateLimit-Remaining'))
        time .sleep(60)
    return left

def project_exists(url):
    r = requests.get(url)
    if r.status_code == 200:
        return True
    return False

def get_source(url, coll, rest):
    page = 1
    project_count = 0
    while True:
        resp = requests.get(url + str(page))
        text = resp.text
        soup = BeautifulSoup(text, 'html.parser')
        if re.search('No results found.', soup.get_text()):
            return

        for link in soup.find_all(class_="project-icon", href=True):
            name = re.findall('/projects/([A-Za-z0-9\-]*)', link.get('href'))
            name = name[0] if name else None
            if name is not None and name.lower().startswith(my_char):
                resp = requests.get(rest + name)
                if resp.status_code == 200:
                    info = json.loads(resp.text)
                    info['forge'] = 'sourceforge'
                    coll.insert_one(info)
                    project_count += 1
                    if project_count >= 50:
                        return
        page += 1
    return

# send queries and extract urls 
def get_gitlab(url, coll):

    global gleft
    global header
    global bginnum
    gleft = wait(gleft)
    values = []
    size = 0
    project_count = 0

    try:
        r = requests .get(url, headers=header)
        time .sleep(0.5)
        # got blocked
        if r.status_code == 403:
            return "got blocked", str(bginnum)
        if (r.ok):

            gleft = int(r.headers.get('RateLimit-Remaining'))
            lll = r.headers.get('Link')
            t = r.text
            array = json.loads(t)
            
            for el in array:
                if el['name'].lower().startswith(my_char):
                    if project_exists(el['http_url_to_repo']):
                        project_count += 1
                        el['forge'] = 'gitlab'
                        coll.insert_one(el)
                        if project_count >= 50:
                            return
            
            #next page
            while ('; rel="next"' in lll):
                gleft = int(r.headers.get('RateLimit-Remaining'))
                gleft = wait(gleft)
                # extract next page url
                ll = lll.replace(';', ',').split(',')
                url = ll[ll.index(' rel="next"') -
                         1].replace('<', '').replace('>', '').lstrip()
             
                try:
                    r = requests .get(url, headers=header)
                    if r.status_code == 403:
                        return "got blocked", str(bginnum)
                    if (r.ok):
                        lll = r.headers.get('Link')
                        t = r.text
                        array1 = json.loads(t)
                        for el in array1:
                            if el['name'].lower().startswith(my_char):
                                if project_exists(el['http_url_to_repo']):
                                    project_count += 1
                                    el['forge'] = 'gitlab'
                                    coll.insert_one(el)
                                    if project_count >= 50:
                                        return
                    else:
                        sys.stderr.write("url can not found:\n" + url + '\n')
                        return
                except requests.exceptions.ConnectionError:
                    sys.stderr.write('could not get ' + url + '\n')

        else:
            sys.stderr.write("url can not found:\n" + url + '\n')
            return

    except requests.exceptions.ConnectionError:
        sys.stderr.write('could not get ' + url + '\n')
    except Exception as e:
        sys.stderr.write(url + ';' + str(e) + '\n')

#start retrieving
get_gitlab(gitlab_url,coll)
get_source(source_url, coll, rest_url)
#print collected data
Fc = 0
for doc in coll.find({}):
	F = open(Fc +".md", "w")
	F.write(doc)
	F.close()
	Fc+=1
