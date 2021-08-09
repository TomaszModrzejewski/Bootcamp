from flask import render_template
from flask import Flask
from flask import request
from flask import redirect

app = Flask(__name__)


@app.route('/mypage/contact', methods=['GET', 'POST'])
def message():
    if request.method == 'GET':
        return render_template("kontakt.html")
    if request.method == 'POST':
        formularz = request.form.getlist("message")
        print(formularz[0])
        return redirect("/mypage/contact")


@app.route('/mypage/me')
def omnie():
    return render_template("index.html")


app.run()
