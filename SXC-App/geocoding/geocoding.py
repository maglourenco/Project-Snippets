import requests


base_url = "https://maps.googleapis.com/maps/api/geocode/json?address="
api_key = "&key=AIzaSyDJQGXd78RWUrPfp3oH1U5okRlNsU4w0_w"
example= "Rua+Central+do+Olival,+nº4162+4415-727,+VILA+NOVA+DE+GAIA+-+PORTO"

response = requests.get(base_url + example + api_key)

location = response.json()['results'][0]['geometry']['location']	# {'lat': 41.053402, 'lng': -8.517332999999999}

print(location['lat'])	
print(location['lng'])

x=dict(address=example,lat=location['lat'], lng=location['lng'])

posto = {}
key = 'Posto ' + '1'
posto[key] = x
print(posto)

