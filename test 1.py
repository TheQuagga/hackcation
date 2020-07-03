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
import requests
import json

def revert(var):
    '''converts any hours outside [0,24] to between regular hours.'''
    if var < 0:
        var += 24
    elif var >= 24:
        var -= 24
    return var

#step 1: departure / arrival date and time
departure_string = "21 June 2018, 3:00" #basic format, liable for change

'''in the form of (year, month, day, hour, minute, second, weekday, day
of the year, and daylight savings)'''
departure = time.strptime(departure_string, "%d %B %Y, %H:%M")
#facilitates changing to seconds after epoch

arrival_string = "21 June 2018, 9:00"
arrival = time.strptime(arrival_string, "%d %B %Y, %H:%M")
redeparture_string = "26 June 2018"
redeparture = time.strptime(redeparture_string, "%d %B %Y")

dep_time = time.mktime(departure) #converts into seconds after epoch
arr_time = time.mktime(arrival)

#step 2: departure / arrival location

def gather_coords(city):
    '''Converts a given city into approximate coordinates in a tuple.'''
    response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address={0}&key=AIzaSyC1PSvX7NUotfAZWY68hT6kgHrtVxrrg8g".format(city))
    data = (json.loads(response.content))["results"][0]["geometry"]["location"]
    return (data["lat"], data["lng"])

depart_city = "Montreal" # input here
arrive_city = "Beijing" # spaces swapped with +

lat1, long1 = gather_coords(depart_city)
lat2, long2 = gather_coords(arrive_city)

def gather_timezone(lat, long, time):
    '''Converts given coordinates into the designated time zone, returning
    hours since UTC.'''
    response = requests.get("https://maps.googleapis.com/maps/api/timezone/json?location={0},{1}&timestamp={2}&key=AIzaSyC1PSvX7NUotfAZWY68hT6kgHrtVxrrg8g".format(lat,long,time))
    data = json.loads(response.content)
    return (data["rawOffset"]) #contains the hours offset from UTC

depart_tz = gather_timezone(lat1, long1, dep_time)
arrive_tz = gather_timezone(lat2, long2, arr_time)
delta = ((arrive_tz - depart_tz)//3600) #difference between dep / arr
print(delta)

#step 3: sleep schedule

sleep_start = 23.0
sleep_end = 7.0

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

#step 4: shift day

shift_day = "19 June 2018"
shift = time.strptime(shift_day, "%d %B %Y")
shift_time = time.mktime(shift)
if shift_time > dep_time: #in case the input is later than the dest.
    shift_time = dep_time #assume that they will not shift earlier

days_before = int((dep_time-shift_time) // 86400) #determines days before dep

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

