from datetime import date, timedelta


def allweekdays(year):
    d = date(year, 11, 18)  # January 1st
    while d.year == year:
        yield d
        d += timedelta(days=7)




if __name__ == '__main__':
    allweekdaystr = ''
    for d in allweekdays(2017):
        # print d.strftime('%Y-%m-%d')
        allweekdaystr += d.strftime('%Y-%m-%d') + ';'
    print allweekdaystr

