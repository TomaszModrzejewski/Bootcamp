from flask import Flask, render_template, request, redirect
import requests
import basicfunctions as bf

response = requests.get(
    "http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

currencies = data[0]["rates"]

new_text = ""
for currency in currencies:
    new_text += f"{currency['currency']};{currency['code']};{currency['bid']};{currency['ask']}\n"

bf.open_currencies("w", new_text)

app = Flask(__name__)


@app.route('/kalkulator/', methods=['GET', 'Post'])
def Kalkulator():
    currencies = bf.currency_names()
    response = "I am waiting for the data..."
    cost = 0
    aktions = ["bid", "get"]
    responses = ["You can knock it out: ", "You have to pay: "]
    if request.method == "POST":
        data = request.form
        currency = data.get('currency')
        amount = float(data.get("amount"))
        bidget = data.get("bidget")
        selektor = aktions.index(bidget)
        rate = float(bf.currdikt()[currency][selektor])
        cost = round(rate*amount*100)/100
        response = f"{responses[selektor]} {cost}PLN"

    return render_template("kalkulator.html", currencies=currencies, response=response)

if __name__ == "__main__":
    app.run(debug=True)
