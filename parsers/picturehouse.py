from typing import Dict, List

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep

from bs4 import BeautifulSoup
from model.film import *

from datetime import date
#from datetime import timedelta

class Picturehouse:

    cinema = "Stratford Picturehouse"
    baseLink = "https://www.picturehouses.com/cinema/stratford-picturehouse"

    whatsOnUrl = baseLink + "WhatsOn?sd={sd}&sm={sm}&sy={sy}&ed={ed}&em={em}&ey={ey}"

    def getFilms(startDate: date, endDate: date) -> List[Screening]:
        url = Picturehouse.getURL()
        soup = Picturehouse.getPage(url)
        films = Picturehouse.getScreenings(soup)
        return films


    def getURL() -> str:   
        return Picturehouse.baseLink

    def getPage(url:str) -> BeautifulSoup:


        options = Options()
        options.headless = True
        options.add_argument('-headless')

        driver = webdriver.Firefox(options=options)
        driver.get(url)
        
        sleep(3)
        return "arrived"
        #return BeautifulSoup(page.content, 'html.parser')
        
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

                screenings.append(Screening(name,time,Picturehouse.cinema,link,screen,notes))
            
        return screenings

url = Picturehouse.getURL()
soup = Picturehouse.getPage(url)
print(soup)
