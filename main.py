import requests
from bs4 import BeautifulSoup
from parsers.pcc import PCC

films = PCC.getFilms("","")

filmDict = dict()
for f in films:
    n = f.name
    if n in filmDict:
        filmDict[n].append(f)
    else:
        filmDict[n] = [f]

for film, screenings in filmDict.items():
    print("---------------")
    print(film)
    for s in screenings:
        print("----")
        print(s.detailString() + ("\n"+s.notes if s.notes else ""))