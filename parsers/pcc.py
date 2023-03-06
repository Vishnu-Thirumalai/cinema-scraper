from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from model.film import *

from datetime import date
from datetime import timedelta

class PCC:

    cinema = "Prince Charles Cinema"
    baseLink = "https://princecharlescinema.com/PrinceCharlesCinema.dll/"

    whatsOnUrl = baseLink + "WhatsOn?sd={sd}&sm={sm}&sy={sy}&ed={ed}&em={em}&ey={ey}"

    def getFilms(startDate: date, endDate: date) -> List[Screening]:
        url = PCC.getURL(startDate, endDate)
        soup = PCC.getPage(url)
        films = PCC.getScreenings(soup)
        return films


    def getURL(startDate: date, endDate: date) -> str:
        """
            Target URL gives all screenings from startDate until (not including) endDate
            If startDate == endDate, it just returns all screenings on that date
            This only includes screenings that have not yet started!
        """
        endDate += timedelta(days=1)
        ret = PCC.whatsOnUrl.format(sd=startDate.day, sm = startDate.month, sy = startDate.year, ed = endDate.day, em = endDate.month, ey = endDate.year)
        return ret

    def getPage(url:str) -> BeautifulSoup:
        page = requests.get(url) 
        return BeautifulSoup(page.content, 'html.parser')
        
    def getScreenings(soup: BeautifulSoup) -> List[Screening]:        
        days = soup.find("div", attrs={'class':'next-7-days-list'}).find_all("div", attrs={'class':'day'}, recursive=False)

        screenings = []
        for day in days:
            curr = day.h4.text
            performances = day.find_all("div", attrs={'class':'performance'})

            for p in performances:
                if p.find("span", attrs={'class':'soldout'}):
                    continue

                main = p.find('a')
                name = main.text.strip()
                link = PCC.baseLink + main.attrs['href']

                time = curr + " - " + p.find("span", attrs={'class':'time'}).text
            
                screen =  p.find("span", attrs={'class':'auditorium'}).text

                notes = p.find("span", attrs={'class':'notes'})
                if notes:
                    notes = notes.text.strip()

                screenings.append(Screening(name,time,PCC.cinema,link,screen,notes))
            
        return screenings
        