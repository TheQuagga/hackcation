'''
delta = 8
sleep_start = 23
sleep_end = 7
days_before = 2
#the above contain the inputs 

if sleep_end < sleep_start: # midnight is passed
    if sleep_end - sleep_start + 24 < 7:
        lbt = sleep_end - 2
    else:
        lbt = sleep_end - 3
elif sleep_end - sleep_start < 7:
    lbt = sleep_end - 2
else:
    lbt = sleep_end - 3
if lbt < 0:
    lbt += 24

change = delta // days_before

'''
import time

def revert(var):
    '''converts any hours outside [0,24] to between regular hours.'''
    if var < 0:
        var += 24
    elif var >= 24:
        var -= 24
    return var

delta = 8 #placeholder for time zone difference input

'''in the form of (year, month, day, hour, minute, second, weekday, day
of the year, and daylight savings)'''
departure_string = "21 June 2018, 3:00" #basic format, could add hour separately
departure = time.strptime(departure_string, "%d %B %Y, %H:%M")
arrival_string = "21 June 2018, 9:00"
arrival = time.strptime(arrival_string, "%d %B %Y, %H:%M")
redeparture_string = "26 June 2018"
redeparture = time.strptime(arrival_string, "%d %B %Y")

'''in the form of (hour, minute)'''
sleep_start = 23.0
sleep_end = 7.0

shift_day = "19 June 2018"
shift = time.strptime(shift_day, "%d %B %Y")

r1 = time.mktime(departure) #converts into seconds after epoch
r2 = time.mktime(shift)

days_before = int((r1-r2) // 86400) #determines days before departure date

change = delta // days_before #determines the necessary shift of sleep

'''the below function defines lowest body temperature point (lbt)'''
if sleep_end < sleep_start: #midnight is passed
    if sleep_end - sleep_start + 24 < 7:
        lbt = sleep_end - 2
    else:
        lbt = sleep_end - 3
elif sleep_end - sleep_start < 7:
    lbt = sleep_end - 2
else:
    lbt = sleep_end - 3
lbt = revert(lbt)
    
for day in range(days_before):
    '''inefficient method: divide time zone delta over days to find average
delay/advance in sleep schedule, ignoring all recommended restrictions'''
    lbt = revert(lbt + change)
    sleep_start = revert(sleep_start + change)
    sleep_end = revert(sleep_end + change)
    print(sleep_start, sleep_end)

''' disregard for now
class Time:
    def __init__(self, string): #in the form HH:MM AM/PM
        self.hour = int(string[0:1])
        self.minute = int(string[2:3])
        if string[4:5] == PM:
            self.hour += 12
            '''

