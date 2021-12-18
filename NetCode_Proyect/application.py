from flask import Flask, request, render_template,redirect, session, url_for, jsonify

from dataRequest import connect, New_Register, Nick_existente, Correct_LogIn, recover_password, Correct_User, login_required, courseData, topicData

import json

from cs50 import SQL

from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from tempfile import mkdtemp
import os

UPLOAD_FOLDER = "./static/images"

app = Flask("__name__")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQL("sqlite:///Users.db")

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
            admin = row[5]

        conn.close() # cerramos la conexcion a la base de datos

        session["user_id"] = User # guardamos la secion

        if admin == 1:
            session["admin"] = session["user_id"]
            return redirect("/admin")
        else:
            return redirect("/User")

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


@app.route("/User")
@login_required
def session_open():

    conn = connect()
    cursor = conn.cursor()

    results = cursor.execute("select * from Curso")

    nombres = []
    img = []
    ids = []
    count = 0

    for r in results:
        ids.append(r[0])
        nombres.append(r[1])
        img.append(r[4])
        count = int(count + 1)


    return render_template("User.html", cursos=count, names=nombres, img=img, Curso_id=ids)


@app.route("/admin")
@login_required
def session_opened():

    conn = connect()

    c = conn.cursor() # creamos un cursor de la coneccion a la base de datos

    # obtenemos el id del usuario logeado
    rows = c.execute("SELECT * FROM Info_Usuario WHERE Id = :id_user", {'id_user':session["user_id"]})
    for row in rows:
        admin = row[5]

    conn.close() # cerramos la conexcion a la base de datos

    if admin == 0:
        return redirect("/User")
    else:
        return render_template("admin.html")

# creacion de formimagenes
global id_a

@app.route("/Almacen/<id_a>")
def Galeria(id_a):
    #Guardando la lista que proporciona la funcion listdir
    listaImagenes = os.listdir(app.config['UPLOAD_FOLDER'])
    print(listaImagenes)
    id_a= (int)(id_a)
    return render_template("Almacen.html", listaImagenes = listaImagenes, id_a=id_a)


@app.route("/formImage/<id_a>", methods= ["GET", "POST"])
@login_required
def subir(id_a):

    #print(id_a)

    if request.method == "POST":

        if not request.files['archivo']:
            return redirect(f"/formImage/{id_a}")

        #Si no existe un archivo
        #if "archivo" not in request.files:
         #   return redirect("/FormImage/"+ id_a)

        archivo = request.files['archivo']

        if archivo.filename == "":
            return redirect(f"/formImage/{is_a}")

        if archivo:
            nombreArchivo = archivo.filename
            archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreArchivo))
            return redirect(f"/Almacen/{id_a}")

        else:
            return redirect(f"/formImage/{id_a}")

    else:
        return render_template("FormImage.html", id_a=id_a)


# Administrar los comenatarios del foro
@app.route("/foro-comentarios", methods= ["GET", "POST"])
@login_required
def foroAdmin():
    return render_template("foro-tabla.html")

@app.route("/Curso/<id>")
@login_required
def Curso(id):

    conn = connect()
    cursor = conn.cursor()
    results = topicData(conn, id)

    nTemas = 0 # aqui guardaremos el numero de temas
    names = [] # aqui guardaremos los nombres de cada tema

    for r in results:
        for c in r:
            try:
                nTemas = int(c) # si es un digito es el numero de temas
            except:
                names.append(c) # sino es el nombre de un tema

    Curso = courseData(conn, id)
    nombreC = "curso"

    for r in Curso:
        for c in r:
            nombreC = c

    content = db.execute(f"SELECT Tema.Contenido FROM Curso INNER JOIN Tema on Tema.Id_Curso=Curso.Id WHERE Curso.Id = {id}")

    #js = json.loads(c)

    js = json.dumps(content, indent=4)

    f = open("Temas.json", "w")
    f.write(js)
    f.close()
    #print(content)

    #jsonify(content)
    conn.close() # cerramos la coneccion a la base de datos

    return render_template("arquitecturaCurso.html", Nombres = names, temas=nTemas, cursoSelected=nombreC, c_id=id)

@app.route("/temaSelected/<nTema>")
def temaSelected(nTema):

    f = open("Temas.json", "r")
    c = f.read()
    js = json.loads(c)

    nTema = int(nTema)

    return jsonify(js[nTema])

@app.route("/foro", methods=["GET", "POST"])
@login_required
def foro():

    if request.method == 'POST':

        if not request.form.get("comentario"):
            return "no puede generar un comentario vacio"

        comment = request.form.get("comentario")

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO ForoComentarios (User_Id, Comment) \
                        values (:user, :comentario)",
                        {'user':session["user_id"], 'comentario':comment})

        conn.commit()
        conn.close()

        return redirect("/foro")

    else:

        conn = connect()
        cursor = conn.cursor()

        comentarios = cursor.execute("select ForoComentarios.Id, ForoComentarios.Comment, ForoComentarios.Date, \
                                    ForoComentarios.Time, Info_Usuario.NickName from ForoComentarios \
                                    inner join Info_Usuario \
                                    on Info_Usuario.Id=ForoComentarios.User_Id")

        ids = []
        nicks = []
        comments = []
        dates = []
        times = []

        count = 0

        for r in comentarios:
            ids.append(r[0])
            nicks.append(r[4])
            comments.append(r[1])
            dates.append(r[2])
            times.append(r[3])

            count = int(count + 1)


        return render_template("Foro.html", results=count, name=nicks, date=dates, time=times, comentario=comments)

@app.route("/ForoRespuesta", methods = ["GET", "POST"])
def ForoRespuesta():

    if request.method == 'POST':

        if not request.form.get("comentario"):
            return "no puede generar un comentario vacio"

        comment = request.form.get("comentario")

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO ForoRespuesta (User_Id, Comment_Id, Answer) \
                        values (:user, comment_id, :comentario)",
                        {'user':session["user_id"], 'comment_id':session["user_id"], 'comentario':comment})

        conn.commit()
        conn.close()

        return redirect("/foro")

    else:
        return render_template("RespuestaForo.html")

@app.route("/eliminarComment/<id_c>")
def eliminarComment(id_c):

    id_c = int(id_c)

    print(f"comment: {id_c}")

    db.execute("delete from ForoComentarios \
                        where Id = :id", id=id_c)

    return redirect("/foro-comentarios")


@app.route("/comentarios")
def comentarios():

    js = db.execute("select Info_Usuario.NickName, ForoComentarios.Comment, ForoComentarios.Id from ForoComentarios \
                                    inner join Info_Usuario \
                                    on Info_Usuario.Id=ForoComentarios.User_Id")
    return jsonify(js)

@app.route("/logout", methods = ["GET", "POST"])
@login_required
def logout():
    if request.method == 'GET':
        # Forget any user_id
        session.clear()

        # Redirect user to login form
        return redirect("/")

    return render_template("Cursos.html")

if __name__== '__main__':
    app.run(debug = True)