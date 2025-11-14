from datetime import date

weekdays = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
dates = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
months = ['January','February','March','April','May','June','July','August','September','October','November','December']
one_for_leap = lambda a: 1 if a == True else 0

year_pattern = {1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',10:'J',11:'K',12:'L',13:'M',14:'N'}


def isLeapYear(year: date.year) -> bool:
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    else:
        return False
    
def getYearPattern(year: date.year):
    return year_pattern[( (year + 5) % 7 ) + one_for_leap(isLeapYear(year)) * 7 + 1]

for a in range(1,10):
    print(getYearPattern(a))