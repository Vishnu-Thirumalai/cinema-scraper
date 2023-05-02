from model.film import Screening

def getFilms():
    films = [Screening(name="Movie {}".format(i))for i in range(5)]
    return films