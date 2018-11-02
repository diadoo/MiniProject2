import sys, re, pymongo, json, time
import datetime
from requests.auth import HTTPBasicAuth
import requests
gleft = 1500

#client = pymongo.MongoClient ()
client = pymongo.MongoClient (host="da1.eecs.utk.edu")
login = sys.argv[1]
passwd = sys.argv[2]

baseurl = 'https://api.github.com/repos'
headers = {'Accept': 'application/vnd.github.v3.star+json'}
headers = {'Accept': 'application/vnd.github.hellcat-preview+json'}

db = client['fdac18mp2'] # added in class
collName = 'releases_jpovlin'
coll = db [collName]
def wait (left):
  while (left < 20):
    l = requests .get('https://api.github.com/rate_limit', auth=(login,passwd))
    if (l.ok):
      left = int (l.headers.get ('X-RateLimit-Remaining'))
      reset = int (l.headers.get ('x-ratelimit-reset'))
      now = int (time.time ())
      dif = reset - now
      if (dif > 0 and left < 20):
        sys.stderr.write ("waiting for " + str (dif) + "s until"+str(left)+"s\n")
        time .sleep (dif)
    time .sleep (0.5)
  return left  

def get (url):
  global gleft
  gleft = wait (gleft)
  values = []
  # sys.stderr.write ("left:"+ str(left)+"s\n")
  try: 
    r = requests .get (url, headers=headers, auth=(login, passwd))
    time .sleep (0.5)
    if (r.ok):
      gleft = int(r.headers.get ('X-RateLimit-Remaining'))
      lll = r.headers.get ('Link')
      links = ['']
      if lll is not None: 
        links = lll.split(',')
  except Exception as e:
    sys.stderr.write ("Could not get:" + url + ". Exception:" + str(e) + "\n")
  return (json.loads(r.text))

def chunks(l, n):
  if n < 1: n = 1
  return [l[i:i + n] for i in range(0, len(l), n)]

def cmp_rel (url):
  v = []
  size = 0
  try: 
    v = get (url)
  except Exception as e:
    sys.stderr.write ("Could not get:" + url + ". Exception:" + str(e) + "\n")
  if 'ahead_by' in v and 'behind_by' in v:
    print (url+';'+str(v['ahead_by'])+';'+str(v['behind_by']))
  else:
    sys.stderr.write ("Could not compare releases for: " + url + "; There exists no common ancestor between the two versions." + "\n")


p2r = {}
for l in sys.stdin.readlines():
  l = l.rstrip()
  p, r = l.split(';')
  if p in p2r: 
    p2r[p] .append (r)
  else: 
    p2r[p] = [r]

for p in p2r:
  rs = p2r[p]
  if len (rs) > 1:
    for i in range(1,len (rs)):
      url = 'https://api.github.com/repos/'+p+'/compare/' + rs[i-1] + '...' + rs[i]
      cmp_rel (url)

