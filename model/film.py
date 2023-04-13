from datetime import datetime

class Screening:
    def __init__(self,name="Movie",time:datetime = datetime(9999,1,1),cinema="cinema",link=None,screen=None,notes=None,duration=0):
        self.name = name
        self.time = time
        self.cinema = cinema
        self.link = link
        self.screen = screen
        self.duration = duration
        self.notes = notes


    def __str__(self):
        ret = self.name + " " + self.time + " " + self.cinema + "\n"


        return  ret + " " + self.screen + "\n" + self.link
    
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

        return  ret

    def getDefault():
        return Screening("Movie","Today","Cinema","www.no.com","Screen 1", None)