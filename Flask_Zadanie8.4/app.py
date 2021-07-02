import flask
from flask import render_template, request, redirect

app = flask.Flask(__name__)


@app.route('/mypage/me')
def my_website():
    return render_template("me.html")


@app.route('/mypage/contact')
def contact():
    return render_template("contact.html")


@app.route('/mypage/contact', methods=['POST'])
def contact_post():
    print(request.form)
    return redirect("/mypage/contact")


if __name__ == '__main__':
    app.run()
