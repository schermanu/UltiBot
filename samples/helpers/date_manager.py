import datetime
import sys


def long_str_to_date(string: str) -> datetime.date:
    naive_date = datetime.datetime.strptime(string, '%A %d %b').date()
    date = appropriate_year(naive_date)
    return date

def compact_str_to_date(string: str) -> datetime.date:
    naive_date = datetime.datetime.strptime(string, '%d/%m').date()
    date = appropriate_year(naive_date)
    return date


def appropriate_year(incomplete_date: datetime.date) -> datetime.date:
    # renvoit la date dont l'année est modifiée de sorte à être dans l'année suivant la reference_date
    # if type(incomplete_date) == datetime.datetime:
    #     incomplete_date = incomplete_date.date()
    reference_date = datetime.date.today() - datetime.timedelta(days=30)
    complete_date = incomplete_date.replace(year=reference_date.year)
    if complete_date < reference_date:
        complete_date = incomplete_date.replace(year=reference_date.year + 1)
    return complete_date
