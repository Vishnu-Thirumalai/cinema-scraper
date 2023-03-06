import requests
from bs4 import BeautifulSoup
from model.film import *

class PCC:

    cinema = "Prince Charles Cinema"
    link = "https://princecharlescinema.com/PrinceCharlesCinema.dll/"

    def getFilms(startDate: str, endDate: str):
        url = PCC.getURL(startDate, endDate)
        soup = PCC.getPage(url)
        films = PCC.getScreenings(soup)
        return films

    #TODO: Pass in dates
    def getURL(startDate: str, endDate: str) -> str:
        return "https://princecharlescinema.com/PrinceCharlesCinema.dll/WhatsOn?sd=5&sm=3&sy=2023&ed=30&em=3&ey=2023"

    def getPage(url) -> BeautifulSoup:
        page = requests.get(url) 
        return BeautifulSoup(page.content, 'html.parser')
        
    def getScreenings(soup: BeautifulSoup):        
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
                link = PCC.link + main.attrs['href']

                time = curr + " - " + p.find("span", attrs={'class':'time'}).text
            
                screen =  p.find("span", attrs={'class':'auditorium'}).text

                notes = p.find("span", attrs={'class':'notes'})
                if notes:
                    notes = notes.text.strip()

                screenings.append(Screening(name,time,PCC.cinema,link,screen,notes))
            
        return screenings
        