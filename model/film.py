class Screening:
    def __init__(self,name="Movie",time="00:00",cinema="cinema",link=None,screen=None,notes=None,duration=0):
        self.name = name
        self.time = time
        self.cinema = cinema
        self.link = link
        self.screen = screen
        self.duration = duration
        self.notes = notes


    def __str__(self):
        return self.name + " " + self.time + " " + self.cinema + " " + self.screen + "\n" + self.link
    
    def detailString(self):
        return self.time + " " + self.cinema + " " + self.screen + "\n" + self.link 

    def getDefault():
        return Screening("Movie","Today","Cinema","www.no.com","Screen 1", None)