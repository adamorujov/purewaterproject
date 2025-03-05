from datetime import date 

def get_date(current_date, time): # time = 0.5, 1, 1.5, 2
    day = current_date.day
    month = current_date.month
    year = current_date.year
    
    if time == 0.5 or time == 1.5:
        if month + 6 <= 12:
            month = month + 6
        else:
            month = month - 6
            year = year + 1
         
        if month in (4, 6, 9, 11) and day == 31:
            day = 30
        elif month == 2 and day > 28:
            day = 28

        if time == 1.5:
            year = year + 1

    else:
        year = year + int(time)
        if month == 2 and day == 29:
            day = 28

    return date(year, month, day)


def is_leap_year(year):
    # If the year is divisible by 4 but not by 100, or if it's divisible by 400, it's a leap year.
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False