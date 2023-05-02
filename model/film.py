from datetime import datetime
from dataclasses import dataclass

@dataclass(order=True) #Generates __lt__(<)/le(<=)/ge/gg based on fields, in order
class Screening:
    time:datetime = datetime(9999,1,1)
    cinema: str ="cinema"
    name: str ="Movie"
    
    link: str =None
    screen: str =None
    notes: str =None
    duration:int = 0
    ageRating: str =None

    def getDefault():
        return Screening("Movie","Today","Cinema","www.no.com","Screen 1", None)
   
    def detailString(self):

        ret = ""
        if self.time:
            ret +=self.time.strftime("%d/%m/%y - %H:%M") + " "
        if self.cinema:
            ret += self.cinema + " "
        if self.screen:
            ret += self.screen + " "
        # if self.link:
        #     ret += "\n" + self.link 

        return ret