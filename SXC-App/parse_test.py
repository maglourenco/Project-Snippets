# ****************************
# GET - Query Objects
# ****************************
import json,http.client

connection = http.client.HTTPConnection('35.180.190.81', 80)
connection.connect()
connection.request('GET', '/parse/classes/Postos_Combustivel', '', {
       "X-Parse-Application-Id": "140692fb9cdff007be0b09aac072a02c84d92dbe"
     })
result = json.loads(connection.getresponse().read())
print(result)

json_res = json.dumps(result, indent=4, sort_keys=True)
print(result)
print("\n\n\n")



# ****************************
# POST - Create Objects
# ****************************
# import json, http.client
#
# connection = http.client.HTTPConnection('35.180.190.81', 80)
# connection.connect()
# connection.request('POST', '/parse/classes/Postos_Combustivel', json.dumps({
#        "latitude": "43.52478",
#        "longitude": "-9.45245",
#        "address": "Rua dos Amores"
#      }), {
#        "X-Parse-Application-Id": "140692fb9cdff007be0b09aac072a02c84d92dbe",
#        "Content-Type": "application/json"
#      })
# results = json.loads(connection.getresponse().read())
# print(results)