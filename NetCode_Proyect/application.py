from flask import Flask, request, render_template
from dataRequest import connect, login, Nick_existente, correct_Sing_In

#como q no

app = Flask("__name__")
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/home")
@app.route("/")
def hello():
    return render_template('Home.html')

@app.route("/login")
def index():
   return render_template("login.html")

if __name__== '__main__':
    app.run(debug = True)