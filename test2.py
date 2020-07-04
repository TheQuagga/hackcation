from flask import Flask, render_template, request, redirect
import time
import requests
import json

app = Flask(__name__)

@app.route('/')
def initialization():
    return render_template('test.html')

@app.route('/', methods = ["POST"])
def signup():
    depart_city = request.form["dest"]
    arrive_city = request.form["arri"]
    departure_string = request.form['d_time']
    arrival_string = request.form["a_time"]
    sleep_start = request.form["sleep"]
    sleep_end = request.form["wake"]
    shift_day = request.form["shift"]
    travel_sleep = request.form.get("plane_sleep")
    alcohol = request.form.get("alcohol")
    coffee = request.form.get("caffeine")
    print(depart_city, arrive_city, departure_string, arrival_string)
    print(sleep_start, sleep_end, shift_day, travel_sleep, alcohol, coffee)
    return redirect('/')

if __name__ == "__main__":
    app.run()

