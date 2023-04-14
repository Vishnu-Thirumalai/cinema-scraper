from typing import Dict, List

from parsers.pcc import PCC
from parsers.picturehouse import PicturehouseCentral, StratfordPicturehouse
from parsers import dummy
from model.film import *
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from dateParser import date


def displayFilms(films:Dict[str,List[Screening]], targetFilm:str = ""):
    for film, screenings in films.items():
        if targetFilm not in film.lower():
            continue
        print("---------------\n---------------")
        print(film)
        print(screenings[-1].ageRating)        
        print(screenings[-1].link)

        screenings.sort(key=lambda x:x.time)

        for s in screenings:
            print("----")
            print(s.detailString() + ("\n"+s.notes if s.notes else ""))


def getFilms(startDate:str, endDate:str) -> Dict[str,List[Screening]]: 
    #films = dummy.getFilms()

    films = PCC.getFilms(startDate,endDate)
    print("Retrieved PCC")

    central = PicturehouseCentral()
    films.extend(central.getFilms(startDate,endDate))
    print("Retrieved Picturehouse Central")

    stratford = StratfordPicturehouse()
    films.extend(stratford.getFilms(startDate,endDate))
    print("Retrieved Picturehouse Stratford")
    

    filmDict = dict()
    for f in films:
        n = f.name.title()
        if n in filmDict:
            filmDict[n].append(f)
        else:
            filmDict[n] = [f]
    return filmDict


helpString = r"""Show movie screenings in London on the given dates.
-------------
Dates must be entered in the format dd/mm/yy, or 'today' or 'tomorrow'
A single date shows all films on that day.
With 2 dates given (seperated by a space) shows films between and including both dates.
Defaults to today with 0 or >2 dates given.

'next week' shows all films in the next seven days."""
def getArgParser() -> ArgumentParser:
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter, 
                            description=helpString)

    #nargs = number of args, '?' is 0/1, * is >=0, + is >=1
    parser.add_argument("dates",help="Dates to search (d.m.y or 'today' or 'tomorrow'). ", default=["today"], nargs='*')
    parser.add_argument("-f","--film",help="Name of film to search for", default="")
    return parser


# Parse CLI arguments
parser = getArgParser()
args = parser.parse_args()
start, end = date.getDatesFromArguments(args.dates)
targetFilm = args.film

print("Searching")
films = getFilms(start, end)
displayFilms(films,targetFilm)