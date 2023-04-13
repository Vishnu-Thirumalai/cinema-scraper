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
from datetime import datetime

class Picturehouse:

    def __init__(self) -> None:
        self.cinema = ""
        self.baseLink = ""

    def getFilms(self, startDate: date, endDate: date) -> List[Screening]:
        url = self.getURL()
        soup = self.getPage(url)
        if soup == None:
            return []
        films = self.getScreenings(soup, startDate, endDate)
        return films


    def getURL(self) -> str:   
        return self.baseLink

    def getPage(self, url:str) -> BeautifulSoup:


        options = Options()
        options.add_argument('-headless')

        driver = webdriver.Firefox(options=options)
        driver.get(url)
        driver.set_window_size(2300,2000)
        

        for i in range(10):
            try:
                get_all_btn = driver.find_element(By.ID,"show_all_dates_btn")
                break
            except NoSuchElementException:
                sleep(1)
        if not get_all_btn:
            print("Can't retrieve films from "+self.cinema+": Get all Dates button missing")
            return None

        get_all_btn.click()
        sleep(10)

        htmlElement = driver.find_element(By.TAG_NAME, "html")
        source = htmlElement.get_attribute("outerHTML")

        soup = BeautifulSoup(source, 'html.parser')

        driver.close()
        driver.quit()

        return soup
        
    def getScreenings(self, soup: BeautifulSoup, startDate: date, endDate: date) -> List[Screening]:
        dates = soup.find('ul',attrs={'id':'show_all_date_list'})

        screenings = []
        while startDate <= endDate:

            #Find div for date
            dateStr = startDate.strftime("class_%Y-%m-%d")
            dateDiv = dates.find("div", attrs={'class':dateStr})
            startDate+= timedelta(days=1)

            if dateDiv == None:
                print("Can't find div for",dateStr)
                continue


            movies = dateDiv.find_all("div", attrs={'class':"movie_deatils_list"})

            for movie in movies:
                m = movie.find("div", attrs={'class':"cinema_ListingBox"})

                movieName = m.a.h3.contents[0].strip()                 
                movieLink = m.a['href']
                movieDuration = m.a.find('span', attrs={'class':"moviMint"}).contents[0].strip()  
                ageRating = m.a.find('span', attrs={'class':"movieNumber_12A"}).contents[0].strip()  

                performances = movie.find("ul", attrs={'class':"cinemaTime_list"}).find_all('li')
                for perf in performances:
                    bookingLink = perf.a['href']
                    t = datetime.strptime(perf.a.span.text.strip(), "%H:%M").time()#24Hour:Minute 
                    movieTime = datetime.combine(startDate, t)

                    notes = ""+ageRating
                    for note in  perf.p.find_all('a'):
                        notes += " "+note.text
                    screenings.append(Screening(movieName,movieTime, self.cinema, movieLink, None, notes, movieDuration))
            
        return screenings


class PicturehouseCentral(Picturehouse):

    def __init__(self) -> None:
        self.cinema = "Picturehouse Central"
        self.baseLink = "https://www.picturehouses.com/cinema/picturehouse-central"


class StratfordPicturehouse(Picturehouse):

    def __init__(self) -> None:
        self.cinema = "Stratford Picturehouse"
        self.baseLink = "https://www.picturehouses.com/cinema/stratford-picturehouse"


# url = Picturehouse.getURL()
# soup = Picturehouse.getPage(url)
# screenings = Picturehouse.getScreenings(soup, date.today(), date.today() + timedelta(days=2))
# for s in screenings:
#     print (s.name +"/"+ str(s.time)+"/"+s.link+" - " + s.notes)


# with open("picturehouse.html") as file:
#     soup = BeautifulSoup(file, 'html.parser')
#     print("parsed")
#     screenings = Picturehouse.getScreenings(soup, date.today(), date.today() + timedelta(days=2))
#     for s in screenings:
#         print (s.name +"/"+ str(s.time)+"/"+s.link+" - " + s.notes)