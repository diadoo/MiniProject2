import sys, json, pymongo, time, datetime, re, requests
from urllib.parse import quote

#for da2 
client = pymongo .MongoClient (host="da1.eecs.utk.edu")
#for gcloud machine
#client = pymongo .MongoClient ()

db = client ['fdac18mp2']

#replace audris with your utkid
coll = db['npm_jpovlin']

pre = 'https://api.npms.io/v2/package/'

def output(s, p):
 print(str(s) + ";" + p)

for pname in sys.stdin.readlines():
 pname = pname.strip('\n')
 #Thks @Macbrine: url parameters need to be quoted
 pname  = quote(pname, safe='')
 r = requests.get(pre + pname)
 if(r.ok):
  result = r.content
  try:
   result_json = json.loads(result.decode('ascii', errors='ignore'))
   #modify keys to remove unwanted '$' '.' characters that mongodb does not allow
   r1 = {}
   for k in result_json:
    k1 = k.replace('$', 'DOLLARSIGN')
    k1 = k1.replace('.', 'PERIODSIGN')
    r1 [k1] = result_json [k]
   coll .insert_one (r1)
   output (0, pname)
  except:
   e = sys.exc_info()[0]
   output (e, pname)
 else:
  output (r .ok, pname)
