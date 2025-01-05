# coding=utf-8
import json, http.client, requests, re, smtplib, codecs
from bs4 import BeautifulSoup
from email.message import EmailMessage
from datetime import datetime

PARSE_SERVER_ID = "140692fb9cdff007be0b09aac072a02c84d92dbe"
ALERT_EMAIL = "mcmiguel_95@hotmail.com"
ALERT_EMAIL2 = "fabiomachuqueiro@gmail.com"
SMTP_EMAIL = "mag.lourenco@campus.fct.unl.pt"
SMTP_PASS = "blhkzyepvamopdel"
PATH = "/home/boardgame-sentinel/sentinel-log.txt"
#PATH = "C:/Users/migue/Desktop/Boardgame Sentinel/sentinel-log.txt"

updated_prices = []
no_price_found_boardgames = []

# Get the data from the Parse Server
def get_database_data():
    conn = http.client.HTTPConnection('35.180.190.81', 80)
    conn.connect()
    conn.request('GET', '/parse/classes/Boardgames', '', {
           "X-Parse-Application-Id": PARSE_SERVER_ID
         })
    return json.loads(conn.getresponse().read().decode('utf-8'))


# Update data on the Parse Server
def update_database_data(new_data):
    conn = http.client.HTTPConnection('35.180.190.81', 80)
    for game in new_data:
        conn.connect()
        conn.request('PUT', '/parse/classes/Boardgames/' + game['objectId'], json.dumps({'preco' : game['preco_novo']}), {
            "X-Parse-Application-Id": PARSE_SERVER_ID,
            "Content-Type": "application/json"
        })
        results = json.loads(conn.getresponse().read().decode('utf-8'))
    print("Dados atualizados com sucesso!")


# Request a shop for a boardgame's price
def request_boardgame_price(link, shop_name):
    # In case is the shop named 'Juegos de la mesa redonda'
    if shop_name == 'Juegos de la mesa redonda':
        try :
            response = requests.get(link, timeout=5)
            if response.status_code == 200 :
                soup = BeautifulSoup(response.content, 'html.parser')
                raw_value = soup.find(id="our_price_display").text
                r = re.compile(r"^\d*[.,]?\d*")
                return float(r.match(raw_value).group(0).replace(',',"."))
            else :
                return None
        except:
            print("Not able to read")
            print({
            	"link" : link,
            	"shop_name": shop_name,
            	"status": "failed"
            	})
            return None
    # In case is either the shop 'Jugamos una' or 'Jugamos otra' (apparently the same owners)
    elif shop_name == 'Jugamos una' or shop_name == 'Jugamos otra' or shop_name == 'Dracotienda':
        try :
            response = requests.get(link, timeout=5)
            if response.status_code == 200 :
                soup = BeautifulSoup(response.content, 'html.parser')
                occurrences = soup.findAll("div", {"class": "current-price"})
                if len(occurrences) > 0:
                	for span in occurrences[0].find_all('span'):
                		if 'content' in span.attrs:
                			return float(span.attrs['content'])
            else :
                return None
        except:
            print("Not able to read")
            print({
            	"link" : link,
            	"shop_name": shop_name,
            	"status": "failed"
            	})
            return None
    # In case is the shop named 'Jogo na mesa'
    elif shop_name == 'Jogo na mesa':
        try :
            response = requests.get(link, timeout=5)
            if response.status_code == 200 :
                soup = BeautifulSoup(response.content, 'html.parser')
                occurrences = soup.findAll("a", {"class": "segmento segmento_reserva"})
                if len(occurrences) > 0:
                    return float(occurrences[0].text[1:])
            else :
                return None
        except:
            print("Not able to read")
            print({
            	"link" : link,
            	"shop_name": shop_name,
            	"status": "failed"
            	})
            return None
    else:
        return "Nome de loja não registado"


# Send an email alert warning of a game price drop
def send_email_alert(game, old_price, email_address):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SMTP_EMAIL, SMTP_PASS)

    # Define the email content
    msg = EmailMessage()
    msg['Subject'] = "Baixa de preço no jogo " + game["nome_jogo"]
    msg['From'] = SMTP_EMAIL
    msg['To'] = email_address
    msg.set_content("Olha só cara, o preço do jogo " + game["nome_jogo"] + " baixou hein! " + "\n\n" + "Preco anterior: " + str(old_price) + " € \n" + "Preco atual: " + str(game["preco"]) + 
    	" € + " + str(game["portes"]) + " € de portes" + "\n" + "Loja: " + game["nome_loja"] + "\n" + "URL: " + game["url_jogo"])
    
    # Send the email
    server.send_message(msg)
    server.close()
    
    print('Email sent to ' + email_address)


# Log the result data
def log_results(updated_prices_data, no_price_found_data):
    with open(PATH, "a+") as f:
        f.write(str(datetime.now()))
        f.write("\n")
        if len(updated_prices) > 0:
        	f.write("UPDATED PRICES\n")
        	json.dump(updated_prices_data, f)
        else:
        	f.write("No price updates")
        f.write("\n")
        if len(no_price_found_boardgames) > 0:
        	f.write("NO PRICE FOUND BOARDGAMES\n")
        	json.dump(no_price_found_data, f)
        else:
        	f.write("No errors finding boardgames prices")
        f.write("\n\n")
        f.close()
        print("Log file updated")



res = get_database_data()
#print(json.dumps(res, indent=4, sort_keys=True))

print("Fetching new prices...")

for game in res["results"]:
    # Get the current boardgame data
    game_url = game["url_jogo"]
    shop_name = game["nome_loja"]
    current_price = game["preco"]
    game_id = game["objectId"]
    game_name = game["nome_jogo"]
    
    # Retrieve the updated price from the boardgame website
    new_price = request_boardgame_price(game_url, shop_name)
    #print(new_price)
    
    if new_price == None:
        continue
    
    # If current price is lower than older price, notify the user via email and update the current price
    if new_price < current_price:
        game["preco"] = new_price
        send_email_alert(game, current_price, ALERT_EMAIL)
        send_email_alert(game, current_price, ALERT_EMAIL2)
        #print("price is LOWER")
        updated_prices.append({
            "objectId": game_id,
            "nome_jogo": game_name,
            "nome_loja": shop_name,
            "preco_antigo": current_price,
            "preco_novo" : new_price,
            "price_var": 'LOWER'
        })
    # If current price is higher than older price, update the current price
    elif new_price > current_price:
        #print("price is HIGHER")
        updated_prices.append({
            "objectId": game_id,
            "nome_jogo": game_name,
            "nome_loja": shop_name,
            "preco_antigo": current_price,
            "preco_novo" : new_price,
            "price_var": 'HIGHER'
        })
    # If the price remains the same, do nothing
    else:
        #print("Price remains the same")
        pass
    
# List of game prices to be updated on the database
#print("Game prices to be updated")
#print(updated_prices)

if len(updated_prices) > 0:
	# Update data on the Parse Server
	update_database_data(updated_prices)

# Log result data
log_results(updated_prices, no_price_found_boardgames)