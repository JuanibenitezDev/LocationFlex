import googlemaps
import os
from dotenv import load_dotenv
from flask import Flask, flash, redirect,render_template, request, url_for
import requests

load_dotenv()

KEY_API = os.getenv("CLIENT_ID")

gmaps = googlemaps.Client(key = KEY_API)
                                                   

def geo_placeid(address):
    url=f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={KEY_API}"
    response= requests.get(url).json()
    response.keys()
    if response['status']=='OK':
        place_id= response['results'][0]['place_id']
        return place_id

def geo_location(address):
    url=f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={KEY_API}"
    response= requests.get(url).json()
    response.keys()
    if response['status']=='OK':
        geometry= response['results'][0]['geometry']
        lat=geometry['location']['lat']
        lng= geometry['location']['lng']
        return f'{lat},{lng}'

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        origin = request.form["origin"]
        if not origin:
            flash('Please enter an origin before submitting.', 'error')
            return redirect('/')
        
        geo_origin = geo_location(origin)
        id_origin = geo_placeid(origin)    
        
        if geo_origin is None or id_origin is None:
            flash('Error processing the origin.', 'error')
            return redirect('/')
        
        flash('Form submitted successfully!', 'success')
        
        return redirect(url_for("result", place_origin=geo_origin, id_origin=id_origin))
    
    else:
        return render_template("index.html", KEY_API=KEY_API)


@app.route('/<id_origin>/<place_origin>')
def result(place_origin,id_origin):
    cord_origin = place_origin
    id_origin = id_origin
    
    return render_template("result.html",cord_origin=cord_origin,id_origin=id_origin,KEY_API=KEY_API)
if __name__ == '__main__':
    app.run()
