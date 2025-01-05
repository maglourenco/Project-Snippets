""" 
	Get the list of gas stations in the ‘Porque Eu Volto’ network of CEPSA in JSON format
	It uses Selenium, a package that automates interaction with the web browser, 
	enabling users to click on the button that shows the gas stations in the ‘Porque Eu Volto’ network of CEPSA. 
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json, http.client
import requests
import re
import json
import time

url = 'https://www.porqueeuvolto.com/wls/porquetuvuelves/jsp/LocalizadorEstaciones'
api_base_url = "https://maps.googleapis.com/maps/api/geocode/json?address="
api_key = "&key=AIzaSyDJQGXd78RWUrPfp3oH1U5okRlNsU4w0_w"
postos_dict = {}
postos_failed = {}
num_results = None
success_results = 0
failed_results = 0

# Method to load the Parse Server database with gas stations
def publish_data_parse_server():
	print("Loading the Parse Server database...")
	connection = http.client.HTTPConnection('35.180.190.81', 80)
	for posto in postos_dict.values():
		connection.connect()
		connection.request('POST', '/parse/classes/Postos_Combustivel', json.dumps(posto), {
		       "X-Parse-Application-Id": "140692fb9cdff007be0b09aac072a02c84d92dbe",
		       "Content-Type": "application/json"
		     })
		results = json.loads(connection.getresponse().read())
		# print(results)
		time.sleep(.100)
	print("Database loading complete!")
	
# Method to show the results of the geocoding operation 
def print_statistics():
	print("\n\n")
	print(" ********** GEOCODING STATS **********")
	print("Total gas stations: " + str(num_results))
	print("Gas stations successfully obtained: " + str(success_results))
	print("Gas stations not available: " + str(failed_results))
	print("\n\n")


print("Getting a list of gas stations...")

driver = webdriver.Chrome("C:\webdrivers\chromedriver.exe") 						# Create a new Chrome session
driver.get(url)
locate_button = driver.find_element_by_id('ctl4') 									# Simulate clicking on button 'Procurar' (Search) to obtain a list of gas stations
locate_button.click() 
soup = BeautifulSoup(driver.page_source, 'html.parser')								# Parse the HTML tags with the gas stations data
postos = soup.find_all('p', {'class' : 'textoZona2 detalle_eess'})
num_results = len(postos)

print("Processing gas stations found...")

for posto in postos:
	time.sleep(.100)														
	nome_posto = posto.text
	key = "Posto " + str(success_results+1)
	address = re.sub('\s+',' ', nome_posto)											# Use RegEx to extract /t and /n's 
	api_address = address.replace(" ", "+")											# Replace spaces with ‘+’ to use the Geocoding API
	try:
		# Create a dictionary of gas stations from which the coordinates were obtained
		response = requests.get(api_base_url + api_address + api_key)
		location = response.json()['results'][0]['geometry']['location']
		data = dict(address=address, lat=location['lat'], lng=location['lng'])
		postos_dict[key] = data
		success_results += 1
	except IndexError:
		# Create a dictionary of gas stations that failed to be retrieved
		postos_failed[key] = dict(
			address=address,
			lat="null", 
			lng="null"
			)
		failed_results += 1
		continue 


publish_data_parse_server()
print_statistics()

result_success = json.dumps(postos_dict, ensure_ascii=False)						# Save a dictionary with successful results in the ‘output_success.txt’ file
output_success = open("output_success.txt", "w", encoding='utf8')					
json.dump(result_success, output_success)
print("***** SUCCESSFUL RESULTS *****")
print(result_success)	

result_failed = json.dumps(postos_failed, ensure_ascii=False)						# Save a dictionary with unsuccessful results in the ‘output_failed.txt’ file
output_failed = open("output_failed.txt", "w", encoding='utf8')					
json.dump(result_failed, output_failed)	
print("***** UNSUCCESSFUL RESULTS *****")
print(result_failed)




    	
    	


