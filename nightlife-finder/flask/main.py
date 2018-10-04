from flask import Flask, request, jsonify
from geojson import FeatureCollection
import googlemaps

app = Flask(__name__)
gmaps = googlemaps.Client(key='AIzaSyB_r4wF5IKxm_flClXaB2P5NoBZ4tTXD3E')

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        nightlife = []
        geoJSON_list = []
        location = request.form['location']
        geocode_result = gmaps.geocode(location)
        # try:
        coords = [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]
        results = gmaps.places('bar, pub, reseraunt', coords)
        if results['status'] == 'OK':
            for result in results['results']:
                try:
                    rating = results['rating']
                except:
                    rating = None
                try:
                    types = results['types']
                except:
                    types = None
                try:
                    price_level = results['price_level']
                except:
                    price_level = None
                try:
                    open_now = results['opening_hours']
                except:
                    open_now = None
                place = {
                    'name': result['name'],
                    'address': result['formatted_address'],
                    'location': result['geometry']['location'],
                    'icon': result['icon'],
                    'open_now': open_now,
                    'image': f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=300&photoreference={result['photos'][0]['photo_reference']}&key=AIzaSyB_r4wF5IKxm_flClXaB2P5NoBZ4tTXD3E",
                    'price_level': price_level,
                    'rating': rating,
                    'types': types
                }
                geoJSON = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [coords[1], coords[0]]
                    },
                    "properties": {
                        "name": result['name'],
                        "image": f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=100&photoreference={result['photos'][0]['photo_reference']}&key=AIzaSyB_r4wF5IKxm_flClXaB2P5NoBZ4tTXD3E",
                        "rating": rating
                    }
                }
                nightlife.append(place)
                geoJSON_list.append(geoJSON)
                geoJSON = {}
                place = {}
        else:
            return 'No results'
        featurecollection = FeatureCollection(geoJSON_list)
        json = {
        'nightlife': nightlife,
        'featurecollection': featurecollection
        }
        return jsonify(json)
    return "<form method='POST'> <input type='text' name='location'> <input type='submit' value='Submit'> </form>"

if __name__ == '__main__':
       app.debug = True
       app.run()
