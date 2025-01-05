import json

with open("output_success.txt") as json_file:
	raw_data = json.load(json_file)

raw_data = raw_data.replace("+", " ")

json_data = json.loads(raw_data)

print(json_data)