import sys
import re
import pymongo
import json
import time
import datetime
import requests

dbname = "fdac18mp2" #please use this database
collname = "glprj_jpovlin" #please modify so you store data in your collection
# beginning page index
begin = "0"
client = pymongo.MongoClient()

db = client[dbname]
coll = db[collname]


beginurl = "https://gitlab.com/api/v4/projects?archived=false&membership=false&order_by=created_at&owned=false&page=" + begin + \
    "&per_page=99&simple=false&sort=desc&starred=false&statistics=false&with_custom_attributes=false&with_issues_enabled=false&with_merge_requests_enabled=false"


gleft = 0

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

# send queries and extract urls 
def get(url, coll):
    print("starting get")
    global gleft
    global header
    global bginnum
    gleft = wait(gleft)
    values = []
    size = 0

    try:
        print("beginning loop")
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
                coll.insert(el)
 
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
                            coll.insert(el)
                    else:
                        sys.stderr.write("url can not found:\n" + url + '\n')
                        return 
                except requests.exceptions.ConnectionError:
                    sys.stderr.write('could not get ' + url + '\n')

        else:
            print("cannot find url")
            sys.stderr.write("url can not found:\n" + url + '\n')
            return

    except requests.exceptions.ConnectionError:
        sys.stderr.write('could not get ' + url + '\n')
    except Exception as e:
        sys.stderr.write(url + ';' + str(e) + '\n')
        
#start retrieving        
get(beginurl,coll)
