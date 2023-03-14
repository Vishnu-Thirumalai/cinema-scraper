from typing import List, Tuple

from datetime import date
from datetime import datetime
from datetime import timedelta


def parseDateArgument(dateStr:str) -> date:
    dateStr = dateStr.lower().strip()
    if dateStr == "today":
        return date.today()
    elif dateStr == "tomorrow":
        return date.today() + timedelta(days=1)
    return datetime.strptime(dateStr, "%d/%m/%y").date()
    
def incrementDate(date: date) -> date:
    return date + timedelta(days=1)


def getDatesFromArguments(dates: List[str]) -> Tuple[date,date]:
    dateStr = " ".join(dates).lower().strip()
    if dateStr == "next week":
        return date.today(), date.today() + timedelta(days=7)

    dates = dateStr.split(" ")
    if len(dates) == 1:
        ret = parseDateArgument(dates[0])
        return (ret,ret)
    elif len(dates) == 2:
        return(parseDateArgument(dates[0]), parseDateArgument(dates[1]))
    else:
        ret =  date.today()
        return (ret,ret)
        