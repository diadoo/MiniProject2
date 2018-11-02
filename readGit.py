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
  size = 0
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
      t = r.text
      size += len (t)
      try:
        array = json .loads (t)
        for el in array:
          values .append (el)
      except Exception as e:
        sys.stderr.write(str(e)+" in json .loads\n")
      #t = r.text.encode ('utf-8')
      while '; rel="next"' in  links[0]:
        gleft = int(r.headers.get ('X-RateLimit-Remaining'))
        gleft = wait (gleft)
        url = links[0] .split(';')[0].replace('<','').replace('>','');
        try: 
          r = requests .get(url, headers=headers, auth=(login, passwd))
          if (r.ok): 
            lll = r.headers.get ('Link')
            links = ['']
            if lll is not None: 
              links = lll .split(',')
            t = r.text
            size += len (t)
            try:
              array = json.loads (t)
              for el in array:
                values .append (el)
              print ('in load next: ' + str(len (values)))
            except Exception as e:
              sys.stderr.write(str(e)+" in json .loads next\n")
          else:
            links = ['']
        except requests.exceptions.ConnectionError:
          sys.stderr.write('could not get ' + links + ' for '+ url + '\n')   
          #print u';'.join((u, repo, t)).encode('utf-8') 
      try: 
        print (url + ';' + str(values))
      except Exception as e:
        sys.stderr.write(str(e)+" in print " + url + "\n")
    else:
      print (url + '\n;ERROR r not ok')
  except requests.exceptions.ConnectionError:
    print (url + ';ERROR ConnectionError')
  print ('returning nkeys=' + str(len (values)))
  return values, size

def chunks(l, n):
  if n < 1: n = 1
  return [l[i:i + n] for i in range(0, len(l), n)]

for n in sys.stdin.readlines():
  #first clean the url
  n = n.rstrip()
  n = re.sub("^.*github.com/","",n)
  n = re.sub("\.git$","",n)
  url = baseurl + '/' + n + '/releases'
  url1 = url
  print("-----------------------------------------------------------------------------------------------------------")
  print("trying to get: " + url1)
  v = []
  size = 0
  try: 
    v, size = get (url1)
    print (str (len (v)) + ';' + str (size) + ';' + url1)
    sys .stdout .flush ()
  except Exception as e:
    sys.stderr.write ("Could not get:" + url1 + ". Exception:" + str(e) + "\n")
    continue
  print (url1 + ' after exception lenv(v)=' + str(len (v)))
  ts = datetime.datetime.utcnow()
  if len (v) > 0:
    # size may be bigger in bson, factor of 2 doesnot always suffice    
    if (size < 16777216/3):
      coll.insert_one ( { 'name': n, 'url': url, 'utc':ts, 'values': v } )
    else:
      s = size;
      n = 3*s/16777216
      i = 0
      for ch in chunks (v, n):
        coll.insert_one ( { 'chunk': i, 'name':n, 'url': url, 'utc':ts, 'values': ch } )
        i = i + 1 
