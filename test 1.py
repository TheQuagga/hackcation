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

'''in the form of (year, month, day, hour, minute, second, weekday, day
of the year, and daylight savings)'''
departure_string = "21 June 2018, 3:00" #basic format
departure = time.strptime(departure_string, "%d %B %Y, %H:%M")
arrival_string = "21 June 2018, 9:00"
arrival = time.strptime(arrival_string, "%d %B %Y, %H:%M")
'''in the form of (hour, minute)'''
sleep_start = (23,0)
sleep_end = (7,0)
result = time.mktime(departure) #converts to secs since epoch
print(result)
result2 = time.mktime(arrival)
print(result2)

class Time:
    def __init__(self, string): #in the form HH:MM AM/PM
        self.hour = int(string[0:1])
        self.minute = int(string[2:3])
        if string[4:5] == PM:
            self.hour += 12

