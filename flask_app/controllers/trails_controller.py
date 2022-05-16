from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.location import Location
from flask_app.models.user import User
import requests
import json


@app.route('/trails/<int:id>')
def trails_location(id):
    data = {
        'id' : id
    }
    main_location = Location.get_by_id(data)

    url = "https://trailapi-trailapi.p.rapidapi.com/trails/explore/"
    # location lat and lon are placed into the api request here
    querystring = {"lat":str(main_location.lat),"lon":str(main_location.lon),"page":"1","per_page":"25"}

    headers = {
        "X-RapidAPI-Host": "trailapi-trailapi.p.rapidapi.com",
        "X-RapidAPI-Key": "4b46476753msh36d31d1f76d51d2p1b512djsnca380eb5f254"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_object = json.loads(response.text)

    trails =  json_object['data']

    data = {
        'user_id' : session['user_id']
    }

    return render_template('display_trails.html', trails = trails, locations = Location.get_all(), main_location = main_location, stashed_trail_ids = User.stashed_trails(data))


@app.route('/trail/display/<int:id>')
def display_trail(id):
    
    url = "https://trailapi-trailapi.p.rapidapi.com/trails/" +str(id)+ ""
    
    headers = {
        "X-RapidAPI-Host": "trailapi-trailapi.p.rapidapi.com",
        "X-RapidAPI-Key": "4b46476753msh36d31d1f76d51d2p1b512djsnca380eb5f254"
    }

    response = requests.request("GET", url, headers=headers)
    json_object = json.loads(response.text)

    trail =  json_object['data']

    return render_template('display_trail.html', trail = trail[0])
