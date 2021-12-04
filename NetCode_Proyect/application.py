from flask import Flask, request, render_template,redirect, session, url_for
from dataRequest import connect, New_Register, Nick_existente, Correct_LogIn, recover_password, Correct_User, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from tempfile import mkdtemp
import os

UPLOAD_FOLDER = "./static/images"

app = Flask("__name__")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/home")
@app.route("/")
def hello():
    return render_template('Home.html')

@app.route("/login", methods= ["POST","GET"])
def login():

    session.clear()

    if request.method == 'POST':

        # validamos que ningun campo este vacio
        if not request.form.get("username"):
            return "error en username"
        elif not request.form.get("password"):
            return "error en password"

        # establecemos la coneccion con la base de datos Users
        conn = connect()

        # validamos que los datos de login sean correctos
        if not Correct_LogIn(conn, request.form.get("password"), request.form.get("username")):
            return "datos erroneos"

        c = conn.cursor() # creamos un cursor de la coneccion a la base de datos

        # obtenemos el id del usuario logeado
        rows = c.execute("SELECT * FROM Info_Usuario WHERE NickName = :nick", {'nick':request.form.get("username")})
        for row in rows:
            User = row[0]

        session["user_id"] = User # guardamos la secion

        conn.close() # cerramos la conexcion a la base de datos

        return redirect("/admin")

    return render_template("login.html")

@app.route("/registro", methods = ["POST","GET"])
def registro():

    if request.method == 'POST':

        # validamos que ningun campo este vacio
        if not request.form.get("name"):
            return "error en name"
        elif not request.form.get("nick"):
            return "error en nick"
        if not request.form.get("email"):
            return "error en email"
        elif not request.form.get("password"):
            return "error en password"

        # establecemos la coneccion con la base de datos Users
        conn = connect()

        #validamos que el nick/username no se repita para varios usuario
        if Nick_existente(conn, request.form.get("nick")):
            return "nic existente"

        # guardamos los nuevos datos del nuevo usuario en la base de datos
        New_Register(conn, request.form.get("name"), request.form.get("nick"), request.form.get("email"), generate_password_hash(request.form.get("password")))

        conn.close() # cerramos la conexcion a la base de datos

        return redirect("/login")


    return render_template("registro.html")


@app.route("/recover", methods = ["GET", "POST"])
def recover():
    if request.method == 'POST':

        if not request.form.get("nickname"):
            return "error en nickname"
        elif not request.form.get("email"):
            return "error en email"
        if not request.form.get("password"):
            return "error en password"
        elif not request.form.get("confirm"):
            return "error en confirm"

        # establecemos la coneccion con la base de datos Users
        conn = connect()

        # si los datos del usuario nos son correctos mostramos un apology
        if not  Correct_User(conn, request.form.get("nickname"), request.form.get("email")):
            return "error en los datos del username & email"

        # si los campos de las password son diferentes mostramos un apology
        if request.form.get("confirm") != request.form.get("password"):
            return "error las contraseñas son diferentes"

        # actualizamos la password en la base de datos
        recover_password(conn, generate_password_hash(request.form.get("password")), request.form.get("nickname"))

        conn.close() # cerramos la conexcion a la base de datos

        return redirect("/login")

    return render_template("recover.html")


@app.route("/Cursos")
@login_required
def session_open():
    return render_template("Cursos.html")

@app.route("/admin")
@login_required
def session_opened():
    return render_template("admin.html")

# creacion de formimagenes

@app.route("/formImage", methods= ["GET", "POST"])
def subir():
    if request.method == "POST":
        #Si no existe un archivo
        if "archivo" not in request.files:
            return redirect("/subir")

        archivo = request.files['archivo']

        if archivo.filename == "":
            return redirect("/subir")

        if archivo:
            nombreArchivo = archivo.filename
            archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreArchivo))
            return redirect("/admin")

        else:
            return redirect("/subir")

    else:
        return render_template("FormImage.html")


# Administrar los comenatarios del foro
@app.route("/foro-comentarios", methods= ["GET", "POST"])
def foroAdmin():
    return render_template("foro-tabla.html")


@app.route("/Python")
@login_required
def Python():
    return render_template("cursoPython.html")

@app.route("/C")
@login_required
def C():

    conn = connect() # conecctamos a la base de datos

    cursor = conn.cursor()

    # obtenemos el numero de temas y los nombres de los temas de un curso
    results = cursor.execute("SELECT Curso.Numero_Temas,  Tema.Nombre FROM Curso INNER JOIN Tema on Tema.Id_Curso=Curso.Id WHERE Curso.Id=2")

    nTemas = 0 # aqui guardaremos el numero de temas
    names = [] # aqui guardaremos los nombres de cada tema

    for r in results:
        for c in r:
            try:
                nTemas = int(c) # si es un digito es el numero de temas
            except:
                names.append(c) # sino es el nombre de un tema

    conn.close() # cerramos la coneccion a la base de datos

    return render_template("cursoC.html", Nombres = names, temas=nTemas)


@app.route("/Java")
def Java():

    conn = connect() # conecctamos a la base de datos

    cursor = conn.cursor()

    # obtenemos el numero de temas y los nombres de los temas de un curso
    results = cursor.execute("SELECT Curso.Numero_Temas,  Tema.Nombre FROM Curso INNER JOIN Tema on Tema.Id_Curso=Curso.Id WHERE Curso.Id=2")

    nTemas = 0 # aqui guardaremos el numero de temas
    names = [] # aqui guardaremos los nombres de cada tema

    for r in results:
        for c in r:
            try:
                nTemas = int(c) # si es un digito es el numero de temas
            except:
                names.append(c) # sino es el nombre de un tema

    conn.close() # cerramos la coneccion a la base de datos

    return render_template("CursoJava.html", Nombres = names, temas=nTemas)

@app.route("/logout", methods = ["GET", "POST"])
def logout():
    if request.method == 'GET':
        # Forget any user_id
        session.clear()

        # Redirect user to login form
        return redirect("/")

    return render_template("Cursos.html")

if __name__== '__main__':
    app.run(debug = True)