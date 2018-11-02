import pymongo, json, sys
client = pymongo.MongoClient (host="da1")
db = client ['fdac18mp2']
id = "jpovlin"
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
