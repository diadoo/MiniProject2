GHUser=diadoo
GHPass=Gra@#11345

rm myurls
rm myrels
rm myurls
#1
zcat /data/NPMvulnerabilities/NPMpkglist/NPMpkglist_31.gz | python3 readNpm.py
#2
python3 extrNpm.py > myurls
#3
python3 readGit.py $GHUser $GHPass < myurls
#4
python3 extrRels.py > myrels
#5
cat myrels | python3 compareRels.py $GHUser $GHPass > myrels.cmp
