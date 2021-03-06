from flask import Flask, render_template, request, redirect
import time
import requests
import json

app = Flask(__name__)

@app.route('/')
def initialization():
    return render_template('test.html')

@app.route('/error')
def error():
    return fail

@app.route('/', methods = ["POST"]) # "/" will link to something else
def signup():
    depart_city = request.form["dest"]
    arrive_city = request.form["arri"]
    departure_string = request.form['d_time']
    arrival_string = request.form["a_time"]
    sleep_start = request.form["sleep"]
    sleep_end = request.form["wake"]
    shift_day = request.form["shift"]
    if request.form.get("plane_sleep") == "on":
        travel_sleep = 1
    else:
        travel_sleep = 0
    if request.form.get("alcohol") == "on":
        alcohol = -1
    else:
        alcohol = 0
    if request.form.get("caffeine") == "on":
        coffee = 1
    elif request.form.get("caffeine_excess") == "on":
        coffee = -1
    else:
        coffee = 0
    print(depart_city, arrive_city, departure_string, arrival_string)
    print(sleep_start, sleep_end, shift_day, travel_sleep, alcohol, coffee)
    #return redirect('/')

    def revert(var):
        '''converts any hours outside [0,24] to between regular hours.'''
        if var < 0:
            var += 24
        elif var >= 24:
            var -= 24
        return var

    #step 1: departure / arrival date and time
    global fail
    try:
        '''in the form of (year, month, day, hour, minute, second, weekday, day
        of the year, and daylight savings)'''
        departure = time.strptime(departure_string, "%Y-%m-%dT%H:%M")
    except:
        fail = "Invalid Departure Date"
        return redirect('/error')

    try:
        arrival = time.strptime(arrival_string, "%Y-%m-%dT%H:%M")
    except:
        fail = "Invalid Departure Date"
        return redirect('/error')
    
    #redeparture_string = "26 June 2018"
    #redeparture = time.strptime(redeparture_string, "%d %B %Y")
    
    dep_time = time.mktime(departure) #converts into seconds after epoch
    arr_time = time.mktime(arrival)

    #step 2: departure / arrival location

    def gather_coords(city):
        '''Converts a given city into approximate coordinates in a tuple.'''
        response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address={0}&key=AIzaSyC1PSvX7NUotfAZWY68hT6kgHrtVxrrg8g".format(city))
        data = (json.loads(response.content))["results"][0]["geometry"]["location"]
        return (data["lat"], data["lng"])

    #depart_city = "Montreal" # input here
    #arrive_city = "Beijing" # spaces swapped with +
    try:
        lat1, long1 = gather_coords(depart_city)
        lat2, long2 = gather_coords(arrive_city)
    except:
        fail = "Invalid Destination / Arrival Places"
        return redirect("/error")

    def gather_timezone(lat, long, time):
        '''Converts given coordinates into the designated time zone, returning
        hours since UTC.'''
        response = requests.get("https://maps.googleapis.com/maps/api/timezone/json?location={0},{1}&timestamp={2}&key=AIzaSyC1PSvX7NUotfAZWY68hT6kgHrtVxrrg8g".format(lat,long,time))
        data = json.loads(response.content)
        return (data["rawOffset"]) #contains the hours offset from UTC

    depart_tz = gather_timezone(lat1, long1, dep_time)
    arrive_tz = gather_timezone(lat2, long2, arr_time)
    delta = ((arrive_tz - depart_tz)//3600) #difference between dep / arr
    if abs(delta) <= 2:
        fail = "Time Zone Difference is not significant enough to dedicate a schedule to prevent jet lag"
        return redirect("/error")
    #print(delta)

    #step 3: sleep schedule

    try:
        sleep_start = int(sleep_start[0:2]) + int(sleep_start[3:5]) / 60 
        sleep_end = int(sleep_end[0:2]) + int(sleep_end[3:5]) / 60
    except:
        fail = "Invalid Sleep Cycle"
        return redirect("/error")

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

    shift = time.strptime(shift_day, "%Y-%m-%d")
    shift_time = time.mktime(shift)
    if shift_time > dep_time: #in case the input is later than the dest.
        shift_time = dep_time #assume that they will not shift earlier

    days_before = min(int((dep_time-shift_time) // 86400), abs(delta)) #determines days before dep
    if days_before == 0:
        fail = "Impossible to generate schedule with 0 days to shift"
        return redirect("/error")
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

    def score(days_before, delta, coffee, alcohol, travel_sleep):
        '''Calculates a score measuring efficiency of the generated jet lag schedule
        based on days dedicated to shifting, coffee and alcohol intake, and sleep
        while travelling.

        coffee = 1 or -1 depending on intake amount
        alcohol = 0 or -1 depending on intake
        travel_sleep = 0 or 1'''

        return (max(days_before, abs(delta)) + coffee*0.2 + alcohol*0.2 + travel_sleep*0.2)

    def schedule(index, change, sleep_start, sleep_end, lbt):
        '''given an index and phase offset, designs a schedule over x days
        in index, returning a tuple with the schedules and the score.'''
        return_schedule = []
        for day in range(index):
            placeholder = []
            lbt = revert(lbt + change)
            sleep_start = revert(sleep_start + change)
            sleep_end = revert(sleep_end + change)
            #print("Local Time")
            placeholder.append(sleep_start)
            placeholder.append(sleep_end)
            #print("Destination Time")
            placeholder.append(revert(sleep_start+delta))
            placeholder.append(revert(sleep_end+delta))
            return_schedule.append(placeholder)
        return (return_schedule, (score(index, delta, coffee, alcohol, travel_sleep)))

    sch1 = schedule(days_before, change, sleep_start, sleep_end, lbt)

    #bonus: scientific score of science


        #these values are arbitrary and can be tuned further

    #bonus2: calculating ideal sleep time for maximum score

    if 0 < delta < 8: #requirements for phase advance
        sch2 = schedule(delta, -1, sleep_start, sleep_end, lbt)
    else: #requirements for phase delaying
        sch2 = schedule(delta//2, 2, sleep_start, sleep_end, lbt)
    file = open("data.txt","w+")
    for x in range(len(sch1[0])):
        file.write("\n")
        for y in range(4):
            file.write(str(sch1[0][x][y])+" ")
    file.write("/n"+str(sch1[1]))
    file.close()

    return redirect('/')

if __name__ == "__main__":
    app.run()

