# Boardgame Sentinel

## Description
Boardgame Sentinel is a tool designed to fetch and monitor the prices of a given list of boardgames across various vendor websites. It stores information about specific boardgames, including the vendors where they are sold and associated shipping costs. The tool periodically retrieves the latest prices from vendor websites and compares them with the prices stored in the Parse Server database. A log report is generated for each periodic check. If prices are different, the database is updated with the most recent prices, regardless of whether they are higher or lower. Additionally, in the event of a price drop, it notifies the user by sending an email alert.

## Features
- Extracts boardgames data from a website using BeautifulSoup.
- Integrates with a custom Parse Server that stores the data about the specific boardgames stored and some vendor websites where they are available.
- Checks the current prices and compares with the stored data; if cheaper, and email alert is sent to a specified email.

## Technologies
- BeautifulSoup (for Web Scraping)
- Parse Server
- AWS EC2
- EmailMessage
- Python

## Status
This tool was developed to automate the monitoring of price changes for specific boardgames across selected vendor websites. However, frequent updates were required due to the highly dynamic nature of boardgame prices and their availability on these websites. Furthermore, the web scraping logic often needed adjustments to accommodate frequent changes in website layouts. As a result, the project was abandoned and sensitive data, such as API keys and credentials, is not hidden within the code.

### Main Files
- **`sentinel_log.txt`**: Stores a log of the tool's checks for price changes.
- **`sentinel.py`** and **`Boardgame Sentinel.ipynb`**: Sample code designed to interact with the custom Parse Server. These snippets perform tasks such as checking the lowest price of a specific boardgame, retrieving updated prices for boardgames using web scraping, logging the results of price checks, and sending email alerts when lower prices are detected for a specific boardgame.