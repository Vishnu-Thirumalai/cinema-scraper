from model.film import Screening

def getFilms():
    films = [Screening.getDefault() for _ in range(5)]
    films[0].name = "Film1"
    return films