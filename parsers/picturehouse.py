from typing import Dict, List

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


from bs4 import BeautifulSoup
from model.film import *

from datetime import date
from datetime import timedelta

class Picturehouse:

    cinema = "Stratford Picturehouse"
    baseLink = "https://www.picturehouses.com/cinema/stratford-picturehouse"


    def getFilms(startDate: date, endDate: date) -> List[Screening]:
        url = Picturehouse.getURL()
        soup = Picturehouse.getPage(url)
        if soup == None:
            return []
        films = Picturehouse.getScreenings(soup, startDate, endDate)
        return films


    def getURL() -> str:   
        return Picturehouse.baseLink

    def getPage(url:str) -> BeautifulSoup:


        options = Options()
        options.add_argument('-headless')

        driver = webdriver.Firefox(options=options)
        driver.get(url)
        driver.set_window_size(2300,2000)
        sleep(0.5)

        try:
            get_all_btn = driver.find_element(By.ID,"show_all_dates_btn")
        except NoSuchElementException:
            print("Can't retrieve films from Picturehouse: Get all Dates button missing")
            return None

        get_all_btn.click()
        sleep(0.5)

        source =driver.page_source

        soup = BeautifulSoup(source, 'html.parser')

        driver.close()
        driver.quit()

        return soup
        
    def getScreenings(soup: BeautifulSoup, startDate: date, endDate: date) -> List[Screening]:
        dates = soup.find('ul',attrs={'id':'show_all_date_list'})

        screenings = []
        while startDate <= endDate:
            dateStr = startDate.strftime("class_%Y-%m-%d")
            startDate+= timedelta(days=1)
            dateDiv = dates.find("div", attrs={'class':dateStr})
            if dateDiv == None:
                continue
            print(dateStr)
            movies = dateDiv.find_all("div", attrs={'class':"movie_deatils_list"})

            for movie in movies:
                m = movie.find("div", attrs={'class':"cinema_ListingBox"})

                movieName = m.a.h3.contents[0].strip()                 
                movieLink = m.a['href']
                movieDuration = m.a.find('span', attrs={'class':"moviMint"}).contents[0].strip()  
                ageRating = m.a.find('span', attrs={'class':"movieNumber_12A"}).contents[0].strip()  

                performances = movie.find("ul", attrs={'class':"cinemaTime_list"}).find_all('li')
                for perf in performances:
                    print(perf)
                    bookingLink = perf.a['href']
                    movieTime = perf.a.span.text.strip()
                    notes = ""+ageRating
                    for note in  perf.p.find_all('a'):
                        notes += " "+note.text
                    screenings.append(Screening(movieName,movieTime, Picturehouse.cinema, movieLink, None, notes, movieDuration))
            
        return screenings

# url = Picturehouse.getURL()
# soup = Picturehouse.getPage(url)

with open("picturehouse.html") as file:
    soup = BeautifulSoup(file, 'html.parser')
    print("parsed")
    screenings = Picturehouse.getScreenings(soup, date.today(), date.today() + timedelta(days=2))
    for s in screenings:
        print (s.name +"/"+ s.time+"/"+s.link+" - " + s.notes)