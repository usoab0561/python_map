import folium
import urllib.request, json
from urllib.parse import quote

# quote를 쓰는이유 : 
# url은 아스키문자(256자)만 넣을수 있는데 한글이 입력되었기 때문이다. (퍼센트인코딩)
# 퍼센트 인코딩(percent-encoding)은 URL에 문자를 표현하는 문자 인코딩 방법이다. 이 방법에 따르면 알파벳이나 숫자 등 몇몇 문자를 제외한 값은 옥텟 단위로 묶어서, 16진수 값으로 인코딩한다.

#Google MapsDdirections API endpoint
endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = ' '

#Asks the user to input Where they are and where they want to go.
origin = quote('독일 프랑크푸르트 시청'.replace(' ','+'))
destination = quote('독일 프랑크푸르트 대학교'.replace(' ','+'))

#Building the URL for the request
nav_request = 'origin={}&destination={}&key={}'.format(origin,destination,api_key)
request = endpoint + nav_request

#Sends the request and reads the response.
response = urllib.request.urlopen(request).read()

#Loads response as JSON
directions = json.loads(response)

#Loads start location(독일프랑푸르트시청) lat and lng
start_location_lat = (directions['routes'][0]['legs'][0]['start_location']['lat'])
start_location_lng = (directions['routes'][0]['legs'][0]['start_location']['lng'])

place_lat = []
place_lng = []

steps_len = len(directions['routes'][0]['legs'][0]['steps'])

# Makes place_lat, place_lng lists
for i in range(steps_len):
    place_lat.append(directions['routes'][0]['legs'][0]['steps'][i]['end_location']['lat'])
    place_lng.append(directions['routes'][0]['legs'][0]['steps'][i]['end_location']['lng'])


# Folium map
m = folium.Map(location=[start_location_lat, start_location_lng],
               zoom_start=14.4)

# Make points
points = []
for i in range(len(place_lat)):
    points.append([place_lat[i], place_lng[i]])

# Make PolyLines
folium.PolyLine(points, color='red').add_to(m)

# Save as map.html
m.save('map.html')
