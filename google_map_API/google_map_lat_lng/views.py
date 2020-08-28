from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Address
import googlemaps
import os

# Create your views here.


"""
Some image pixel to lat & lng calculations:
92, 16
965, 418
(965 - 92) / (-70.034949 + 73.344234) = 263.80 X pixel/lng
(418 - 16) / (42.854226 - 41.722659) = 355.26 Y pixel/lat
Lat & lng at top left corner:
lat: 28 / 609.77 + 42.854226 = 42.900
lng: 92 / 263.80 - 73.344234 = 73.693
"""
# Some parameters to set map rendering.
img_top_left_lat = 42.9
img_top_left_lng = -73.693
x_pixel_per_lng = 263.8
y_pixel_per_lat = 355.26
map_pin_width = 32
map_pin_height = 32

img_zoom_factor = 1

def google_map_lat_lng(request):
    # return HttpResponse('google_map_lat_lng')
    context = {
        'res': 'Missing Input',
        'has_result': False
    }
    return render(request, 'google_map_lat_lng/index.html', context)

def look_up(request):
    try:
        raw_address_str = str(request.POST['raw_address'])
    except KeyError:
        return Http404('Raw address incorrect!')

    if len(raw_address_str) == 0:
        context = {
            'res': 'Need Input',
            'has_result': False
        }

    else:
        BASE = os.path.dirname(os.path.abspath(__file__))
        key = open(os.path.join(BASE, 'gmap_key.txt'), 'r').read() # Use your own Google map API key:
        # https://developers.google.com/maps/documentation/geocoding/get-api-key

        gmap_client = googlemaps.Client(key=key)

        res = gmap_client.geocode(raw_address_str)

        if len(res) == 0:
            context = {
                'res': 'No valid match on Google Maps API!',
                'has_result': False
            }

        else:
            try:
                geocoded_address = res[0]['formatted_address']
                lat = res[0]['geometry']['location']['lat']
                lng = res[0]['geometry']['location']['lng']

                try:
                    state = [x['short_name'] for x in res[0]['address_components'] if 'administrative_area_level_1' in x['types']][0]
                    if state == 'MA':
                        inside_ma = True
                    else:
                        inside_ma = False

                except IndexError:
                    state = 'Not Found!'
                    inside_ma = False
                except Exception as e:
                    state = 'N/A'
                    inside_ma = False

                pointer_loc_x_pixel = int(((float(lng) - img_top_left_lng) * x_pixel_per_lng) * img_zoom_factor) - map_pin_width / 2
                pointer_loc_y_pixel = int(((img_top_left_lat - float(lat)) * y_pixel_per_lat) * img_zoom_factor) - map_pin_height
                context = {
                        'res': 'Valid Google Maps result!',
                        'input_address': raw_address_str,
                        'geocoded_address': geocoded_address,
                        'inside_ma': inside_ma,
                        'lat': lat,
                        'lng': lng,
                        'pointer_loc_x_pixel': pointer_loc_x_pixel,
                        'pointer_loc_y_pixel': pointer_loc_y_pixel,
                        'has_result': True
                    }

            except Exception as e:
                context = {
                        'res': 'No valid match on Google Maps API!',
                        'has_result': False
                    }

    return render(request, 'google_map_lat_lng/index.html', context)
