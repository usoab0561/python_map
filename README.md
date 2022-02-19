# google map api 경로 호출 후, folium으로 선형데이터 html로 save

## 사용 : google cloud platform, directions API, folium, vscode, python 3.9.10  

Google could platform에서   

Directions API 를 사용해줌.  
##Direction API란?   
(HTTP 요청을 사용하여 Directions API로 운전, 자전거 타기, 도보 및 대중교통 라우팅에 액세스합니다. 웨이포인트는 특정 위치를 통과하는 경로를 변경할 수 있는 기능을 제공합니다. 출발지, 목적지 및 경유지를 텍스트 문자열(예: "Chicago, IL" 또는 "Darwin, NT, Australia") 또는 위도/경도 좌표로 지정합니다.)  
  
![image](https://user-images.githubusercontent.com/84604563/154814504-7f9d39ec-3fa6-4ac2-a4fa-82e25fb1c0f9.png)
api_key를 생성, quote사용해서 퍼센트인코딩 해준다.  
> quote를 쓰는이유 :   
> url은 아스키문자(256자)만 넣을수 있는데 한글이 입력되었기 때문이다. (퍼센트인코딩)  
>퍼센트 인코딩(percent-encoding)은 URL에 문자를 표현하는 문자 인코딩 방법이다. 이 방법에 따르면 알파벳이나 숫자 등 몇몇 문자를 제외한 값은 옥텟 단위로 묶어서, 16진수 값으로 인코딩한다.  

<br>

<img width="882" alt="#Building the URL for the request" src="https://user-images.githubusercontent.com/84604563/154813508-ae524f3f-26eb-48b2-8222-42bcabc2b022.png">
 request를 위한 URL을 만들어주고  
<br>

<img width="539" alt="#Sends the request and reads the response" src="https://user-images.githubusercontent.com/84604563/154813512-25deb8ab-4b9b-435e-bc2e-6d5718edaefb.png">
Request 받아 읽고, json으로 가져온다.

<br>

json으로 가져온 direction을 살펴보면, 다음과 같다. 
<img width="1391" alt="Pasted Graphic 9" src="https://user-images.githubusercontent.com/84604563/154813517-bb8cf967-521f-4084-829c-12d8716faa2c.png">
routes 밑에 legs가 있고, legs안에 start_location과 end_location,   
그리고 steps안에 start_location과 end_location(lat, lng)가 들어있다.  

<br>

일단 start_location(독일프랑푸르트시청의 lat, lng을 가져와주고)  
<img width="863" alt="lat and" src="https://user-images.githubusercontent.com/84604563/154813530-c2a86f18-8195-43d1-b130-4a0e25170b90.png">
<br>

steps_len을 구해 그 개수만큼 place_lat에 end_location의 lat을 넣어주고,  
place_lng에 lng를 넣어준다. append를 사용해서 순서대로 넣어준다.  
<img width="807" alt="Pasted Graphic 12" src="https://user-images.githubusercontent.com/84604563/154813539-6de71732-c06b-4d56-9aec-b788b84ad4d4.png">

<br>

Folium에서 map 사용해서 지도 불러와주고 points에 위도 경도 넣어준다.  
<img width="584" alt="zoom_start=14 4)" src="https://user-images.githubusercontent.com/84604563/154813544-7aeccf2b-d5cf-4101-ae4f-acee15e54c4e.png">

<br>

<img width="413" alt="Pasted Graphic 15" src="https://user-images.githubusercontent.com/84604563/154813546-d27ae1c0-f608-4ff3-8906-e74ba6446f5d.png">
경로선형을 넣어주고  
<br>

<img width="167" alt="Pasted Graphic 16" src="https://user-images.githubusercontent.com/84604563/154813548-efcd3355-d689-41f8-bdf6-fd8344b87af5.png">
html로 저장해준다.  

다음은 결과다.<br>
<img width="1431" alt="Pasted Graphic 13" src="https://user-images.githubusercontent.com/84604563/154813550-9b1260e6-5001-48a1-ad70-b1be3ad0f74f.png">

<br>


Python 전체코드
```python
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

```

html결과코드
```html
<!DOCTYPE html>
<head>    
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    
        <script>
            L_NO_TOUCH = false;
            L_DISABLE_3D = false;
        </script>
    
    <style>html, body {width: 100%;height: 100%;margin: 0;padding: 0;}</style>
    <style>#map {position:absolute;top:0;bottom:0;right:0;left:0;}</style>
    <script src="https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.js"></script>
    <script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css"/>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css"/>
    
            <meta name="viewport" content="width=device-width,
                initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
            <style>
                #map_180cbb62286744f6a3112139ab2589d5 {
                    position: relative;
                    width: 100.0%;
                    height: 100.0%;
                    left: 0.0%;
                    top: 0.0%;
                }
            </style>
        
</head>
<body>    
    
            <div class="folium-map" id="map_180cbb62286744f6a3112139ab2589d5" ></div>
        
</body>
<script>    
    
            var map_180cbb62286744f6a3112139ab2589d5 = L.map(
                "map_180cbb62286744f6a3112139ab2589d5",
                {
                    center: [50.1108836, 8.682001399999999],
                    crs: L.CRS.EPSG3857,
                    zoom: 14.4,
                    zoomControl: true,
                    preferCanvas: false,
                }
            );

            

        
    
            var tile_layer_b9f29f53b6e1489d995dfbb98837330a = L.tileLayer(
                "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                {"attribution": "Data by \u0026copy; \u003ca href=\"http://openstreetmap.org\"\u003eOpenStreetMap\u003c/a\u003e, under \u003ca href=\"http://www.openstreetmap.org/copyright\"\u003eODbL\u003c/a\u003e.", "detectRetina": false, "maxNativeZoom": 18, "maxZoom": 18, "minZoom": 0, "noWrap": false, "opacity": 1, "subdomains": "abc", "tms": false}
            ).addTo(map_180cbb62286744f6a3112139ab2589d5);
        
    
            var poly_line_d3cf181e49be4427b764526df6abf9ce = L.polyline(
                [[50.1108833, 8.6820001], [50.1108057, 8.681273599999999], [50.1105159, 8.6794674], [50.111195, 8.679433399999999], [50.11105329999999, 8.678516900000002], [50.110132, 8.677322], [50.1094749, 8.6745497], [50.1134114, 8.6717678], [50.1138601, 8.6700559], [50.11538119999999, 8.6710503], [50.11667869999999, 8.6710701], [50.1234162, 8.6699291], [50.1242808, 8.6700064], [50.1240909, 8.668012599999999]],
                {"bubblingMouseEvents": true, "color": "red", "dashArray": null, "dashOffset": null, "fill": false, "fillColor": "red", "fillOpacity": 0.2, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1.0, "smoothFactor": 1.0, "stroke": true, "weight": 3}
            ).addTo(map_180cbb62286744f6a3112139ab2589d5);
        
</script>
```
