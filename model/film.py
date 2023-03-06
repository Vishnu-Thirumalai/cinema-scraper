class Screening:
    def __init__(self,name,time,cinema,link,screen,notes):
        self.name = name
        self.time = time
        self.cinema = cinema
        self.link = link
        self.screen = screen
        self.notes = notes


    def __str__(self):
        return self.name + " " + self.time + " " + self.cinema + " " + self.screen + "\n" + self.link
    
    def detailString(self):
        return self.time + " " + self.cinema + " " + self.screen + "\n" + self.link 
