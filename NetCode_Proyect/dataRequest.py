import sqlite3
from sqlite3 import Error

def connect():
    """Conecta la Base de datos"""

    try:
        conn = sqlite3.connect('Users.db')
        print("Successfull connection")
        return conn
    except Error:
        print(Error)

def login(conn, name, nickN, email, passw, lastN):
    """Ingresa un nuevo usuario a la base de datos"""

    cursor = conn.cursor()
    cursor.execute(" INSERT INTO Info_Usuario(Name, NickName, EmailAddres, Password, LastName) VALUES(:Name, :NickName, :EmailAddres, :Password, :LastName)",
                                        {'Name':name, 'NickName':nickN,
                                        'EmailAddres':email, 'Password':passw, 'LastName':lastN})
    conn.commit()

def Nick_existente(conn, nickN):
    """Verifica si un NickName ya existe"""

    cursor = conn.cursor()

    resultados = cursor.execute(f" SELECT NickName FROM Info_Usuario WHERE NickName = '{nickN}'")

    for resultado in resultados:
        for clave in resultado:
            if clave == nickN:
                return True

    return False

def correct_Sing_In(conn, password, nickN):
    """Verifica que los datos de un inicio de secion sean correctos"""

    cursor = conn.cursor()

    resultados = cursor.execute(f" SELECT NickName, Password FROM Info_Usuario WHERE NickName = '{nickN}' AND Password = '{password}'")

    Nick = False
    Pssw = False

    for resultado in resultados:
        for clave in resultado:
            if clave == nickN:
                Nick = True
            elif clave == password:
                Pssw = True

    if Nick == True and Pssw == True:
        return True
    else:
        return False

