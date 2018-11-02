import pymongo, json, sys
client = pymongo.MongoClient (host="da1")
db = client ['fdac18mp2']
id = "jpovlin"
coll = db [ 'releases_' + id]
for r in coll.find():
  n = r['name']
  if 'values' in r:
    for v in r['values']:
      if 'tag_name' in v:
        print (n+';'+v['tag_name'])
