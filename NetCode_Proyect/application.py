from flask import Flask, request, render_template,redirect
from dataRequest import connect, login, Nick_existente, correct_Sing_In

# prueba para el git

app = Flask("__name__")
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/home")
@app.route("/")
def hello():
    return render_template('Home.html')

@app.route("/login", methods= ["POST","GET"])
def login():

    if request.method == 'POST':
        name = request.form.get("name")
        password = request.form.get("password")

        #se debe de verificar si existe o no


        #redireccionamos al contenido

    else:
        return render_template("login.html")

    return render_template("login.html")

@app.route("/registro", methods = ["POST","GET"])
def registro():

    if request.method == 'GET':
        return render_template("registro.html")

    else:
        
        conn = connect()
        
        #hacer las debidas condiciones para saber si se ha ingresado correctamente
        
        name = request.form.get("name")
        password = request.form.get("password")
        email = request.form.get("email")
        
        
        return render_template("login.html")

    return redirect('/registro')



if __name__== '__main__':
    app.run(debug = True)