from serpapi import GoogleSearch
from geopy.geocoders import Nominatim
 

geolocator = Nominatim(user_agent="my_user_agent")

def get_nearby(location):

    loc = geolocator.geocode(location)
    print(loc)
    params = {
    "engine": "google_maps",
    "q": "Hospital",
    "ll": f"@{loc.latitude},{loc.longitude},15z",
    "type": "search",
    "api_key": ""
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    
    hospital_info = []
    for result in results['local_results']:
        try:
            hospital_info.append((result['title'],result['phone'],result['thumbnail'],result['gps_coordinates']))
        except:
            pass

    return hospital_info[0:5]

