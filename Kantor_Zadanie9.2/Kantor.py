from urllib import request
import json

address = 'http://api.nbp.pl/api/exchangerates/tables/A/?format=json'

# response = request.urlopen(address)
# print(response.read())

with request.urlopen(address) as response:
    data = response.read()
    data = json.loads(data)
    waluty = data[0]['rates']

    for waluta in waluty:
        print(f"{waluta['code']} - przelicznik: {waluta['mid']}")

co = input('Jaką walutę chcesz kupić? ').upper()
ile = int(input(f'Ile złotówek chcesz wymienić ?'))

for waluta in waluty:
    if waluta['code'] == co:
        wymiana = ile / waluta['mid']
        print(f"{waluta['code']} po {waluta['mid']}. Wymieniasz {ile} PLN dostajesz {round(wymiana,2)} {waluta['code']}")
