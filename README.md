# MiniProject2: Phase2: Store info on NPM packages in MongoDB

## Task: Getting Release info from GitHub on NPM packages

### Resources:
NPM package list

The list of packages is unique to each one of you:
/data/NPMvulnerabilities/NPMpkglist/NPMpkglist_XX.gz
where XX is between 0 and 33: to find your number look at the list below. 

### Goal:
1. Download and store data from npm on all your packages on mongodb database:
    fdac18mp2, collection: npm_yourutkid, the example code is in readNpm.py
```
zcat /data/NPMvulnerabilities/NPMpkglist/NPMpkglist_XX.gz | python3 readNpm.py
```
Please keep in mind that /data/NPMvulnerabilities/ is not on gcloud, only 
on da2, so please run it on da2 or copy NPMpkglist_XX.gz to gcloud.

2. Identify the packages that have GH repos (based on the stored info)
```
import pymongo, json, sys
client = pymongo.MongoClient ()
db = client ['fdac18mp2']
id = sys.argv[1] #your utkid
coll = db [ 'npm_' + id]
for r in coll.find():
  if 'collected' in r:
    r = r['collected']
    if 'metadata' in r:
      r = r['metadata']
      if 'repository' in r:
        r = r['repository']
        if 'url' in r:
          r = r['url']
          print (r)
```
The above code is in extrNpm.py. To output the urls:
```
python3 extrNpm.py > myurls
```

3. For each such package, get a list of all releases.  Example file is readGit.py (you can use it with the snippet above to get releases). It reads from standard input and populates
releases_yourutkid collection. Reference to Github API: 
```
cat myurls | python3 readGit.py 
#or
python3 readGit.py < myurls
```
4. Extract releases from mongodb
```
import pymongo, json, sys
client = pymongo.MongoClient (host="da1")
db = client ['fdac18mp2']
id = "audris"
coll = db [ 'releases_' + id]
for r in coll.find():
  n = r['name']
  if 'values' in r:
    for v in r['values']:
      if 'tag_name' in v:
        print (n+';'+v['tag_name'])
```          
The above code is in extrRels.py. To output the urls:
```
python3 extrRels.py > myrels
```


5. Find no. of commits between the latest and other releases.

For example:
    E.g. https://api.github.com/repos/webpack-contrib/html-loader/compare/v0.5.4...master or https://api.github.com/repos/git/git/compare/v2.2.0-rc1...v2.2.0-rc2
    More resource: https://stackoverflow.com/questions/26925312/github-api-how-to-compare-2-commits (look for comparing the tags in the answer)
    Get the data from the json, look for something like to get no. of commits between releases
```    
 "status": "ahead",
 "ahead_by": 24,
 "behind_by": 0,
 "total_commits": 24,
```
For example
```
cat myrels | python3 compareRels.py > myrels.cmp
```
 
| number  | GitHub Username | NetID | Name |
|:-:|:-:|:-:|---|
| 0 | 3PIV | pprovins | Provins IV, Preston |
| 1 | BrettBass13 | bbass11 | Bass, Brett Czech |
| 2 | CipherR9 | gyj992 | Johnson, Rojae Antonio |
| 3 | Colsarcol | cmawhinn | Mawhinney, Colin Joseph |
| 4 | EvanEzell | eezell3 | Ezell, Evan Collin |
| 5 | MikeynJerry | jdunca51 | Duncan, Jerry |
| 6 | Tasmia | trahman4 | Rahman, Tasmia |
| 7 | awilki13 | awilki13 | Wilkinson, Alex Webb |
| 8 | bryanpacep1 | jpace7 | Pace, Jonathan Bryan |
| 9 | caiwjohn | cjohn3 | John, Cai William |
| 10 | cflemmon | cflemmon | Flemmons, Cole |
| 11 | dbarry9 | dbarry | Barry, Daniel Patrick |
| 12 | desai07 | adesai6 | Desai, Avie |
| 13 | gjones1911 | gjones2 | Jones, Gerald Leon |
| 14 | herronej | eherron5 | Herron, Emily Joyce |
| 15 | hossain-rayhan | rhossai2 | Hossain, Rayhan |
| 16 | jdong6 | jdong6 | Dong, Jeffrey Jing |
| 17 | jyu25utk | jyu25 | Yu, Jinxiao |
| 18 | mkramer6 | mkramer6 | Kramer, Matthew S |
| 19 | mmahbub | mmahbub | Mahbub, Maria |
| 20 | nmansou4 | nmansou4 | Mansour, Nasib |
| 21 | nschwerz | nschwerz | Schwerzler, Nicolas Winfield William |
| 22 | rdabbs42 | rdabbs1 | Dabbs, Rosemary |
| 23 | saramsv | mousavi | Mousavicheshmehkaboodi, Sara |
| 24 | spaulsteinberg | ssteinb2 | Steinberg, Samuel Paul |
| 25 | zol0 | akarnauc | Karnauch, Andrey |
| 26 | zrandall | zrandall | Randall, Zachary Adams |
| 27 | lpassarella | lpassare | Passarella, Linsey Sara |
| 28 | tgoedecke | pgoedec1 | Goedecke, Trish |
| 29 | ray830305 | hchang13 | Chang, Hsun Jui |
| 30 | ssravali | ssadhu2 | Sadhu, Sri Ravali |
| 31 | diadoo | jpovlin | Povlin, John P |
| 32 | mander59 | mander59 | Anderson, Matt Mcguffee |
| 33 | iway1 | iway1 | Way, Isaac Caldwell |

# MiniProject2: Phase1: Discover a list of projects on SourceForge.net and GitLab.com


These two forges present two different types of data discovery challenges. 

SourceForge actively prevents discovery. Over ten years ago it was the largest forge 
but as it started losing market share to other forges, they started blocking project discovery. 

GitLab, on the other hand, has an error-prone API that is highly unreliable. 


## Part 1
 - Discover at least 50 projects on SourceForge and GitLab whose 
names start with the letter (case insensitive) in front of your name in the list below.
 - Provide the IPython notebook you used to discovery the data.

You are free to use any method, including a list compiled by someone else, search on google search engine, etc. 
but you do need to verify that the discovered projects currently exist on these 
forges by retrieving the url of the version control repository used by the project.

Please use the Google Cloud VM when discovering the project names to avoid accidentally 
causing UTK to be blocked. 

| Letter  | GitHub Username | NetID | Name |
|:-:|:-:|:-:|---|
| a | 3PIV | pprovins | Provins IV, Preston |
| b | BrettBass13 | bbass11 | Bass, Brett Czech |
| c | CipherR9 | gyj992 | Johnson, Rojae Antonio |
| d | Colsarcol | cmawhinn | Mawhinney, Colin Joseph |
| e | EvanEzell | eezell3 | Ezell, Evan Collin |
| f | MikeynJerry | jdunca51 | Duncan, Jerry |
| g | Tasmia | trahman4 | Rahman, Tasmia |
| h | awilki13 | awilki13 | Wilkinson, Alex Webb |
| i | bryanpacep1 | jpace7 | Pace, Jonathan Bryan |
| j | caiwjohn | cjohn3 | John, Cai William |
| k | cflemmon | cflemmon | Flemmons, Cole |
| l | dbarry9 | dbarry | Barry, Daniel Patrick |
| m | desai07 | adesai6 | Desai, Avie |
| n | gjones1911 | gjones2 | Jones, Gerald Leon |
| o | herronej | eherron5 | Herron, Emily Joyce |
| p | hossain-rayhan | rhossai2 | Hossain, Rayhan |
| q | jdong6 | jdong6 | Dong, Jeffrey Jing |
| r | jyu25utk | jyu25 | Yu, Jinxiao |
| s | mkramer6 | mkramer6 | Kramer, Matthew S |
| t | mmahbub | mmahbub | Mahbub, Maria |
| u | nmansou4 | nmansou4 | Mansour, Nasib |
| v | nschwerz | nschwerz | Schwerzler, Nicolas Winfield William |
| w | rdabbs42 | rdabbs1 | Dabbs, Rosemary |
| x | saramsv | mousavi | Mousavicheshmehkaboodi, Sara |
| y | spaulsteinberg | ssteinb2 | Steinberg, Samuel Paul |
| z | zol0 | akarnauc | Karnauch, Andrey |
| a | zrandall | zrandall | Randall, Zachary Adams |
| b | lpassarella | lpassare | Passarella, Linsey Sara |
| c | tgoedecke | pgoedec1 | Goedecke, Trish |
| d | ray830305 | hchang13 | Chang, Hsun Jui |
| e | ssravali | ssadhu2 | Sadhu, Sri Ravali |
| f | diadoo | jpovlin | Povlin, John P |
| g | mander59 | mander59 | Anderson, Matt Mcguffee |
| h | iway1 | iway1 | Way, Isaac Caldwell |

## GitLab discovery  
GitLab provides [APIs](https://docs.gitlab.com/ee/api/) to retrieve project urls.  
Here is sample code for collecting project urls (and storing data in mongodb):
```
import sys
import re
import pymongo
import json
import time
import datetime
import requests

dbname = "fdac18mp2" #please use this database
collname = "glprj_yourutkid" #please modify so you store data in your collection
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

    global gleft
    global header
    global bginnum
    gleft = wait(gleft)
    values = []
    size = 0

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
            sys.stderr.write("url can not found:\n" + url + '\n')
            return

    except requests.exceptions.ConnectionError:
        sys.stderr.write('could not get ' + url + '\n')
    except Exception as e:
        sys.stderr.write(url + ';' + str(e) + '\n')
        
#start retrieving        
get(beginurl,coll)
```

Note that the parameters in the sample code are not optimal. Please feel free to tune them. This sample code is not robust enough to deal with various returned errors from query. You might need to investigate errors encountered individually.
