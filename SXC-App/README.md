# SXC App

## Description
SXC App is a tool for obtaining a list of gas stations in the 'Porque Eu Volto' network of CEPSA in JSON format. It uses Selenium, a Python package that automates interactions with web browsers, to dynamically interact with the website. This tool was intended to be part of a larger system designed to retrieve gas stations near a user's location from CEPSA. It automates the process of clicking the button that reveals the gas stations in the 'Porque Eu Volto' network, making the data easily accessible for further use.

## Features
- Automates web interactions using Selenium.
- Extracts gas station data from a website using BeautifulSoup and formats it into JSON format.
- Integrates with a custom Parse Server to store the gas stations' data.
- Uses the Google Geocoding API to convert geographic addresses into geographic coordinates.

## Technologies
- Selenium and BeautifulSoup (for Web Scraping)
- Parse Server
- AWS EC2
- Google Geocoding API
- Python

## Status
This tool was developed to support a website that is no longer live. As a result, the tool is not currently functional, and sensitive data, such as API keys and credentials, is not hidden within the code.


### Main Files
- **`postos_script.py`**: Contains most of the implementation code for automating interactions with the CEPSA website.
- **`geocoding.py`**: Used to extract data from the Google Geocoding API.
- **`parse_test.py`** and **`parse_db.ipynb`**: Sample code to interact with the custom Parse Server.
