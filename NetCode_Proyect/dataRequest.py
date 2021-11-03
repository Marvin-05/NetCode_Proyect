import sqlite3
import sys
from sqlite3 import Error

def connect():
    """Conecta la Base de datos"""

    # usamos un try except para tratar de conectar la base datos y en caso de error dejar de ejeccutar el programa e imprimir el error
    try:
        # sqlite3.connect('nombre.db') conecta la base de datos a traves de la variable conn (la variable 'conn' puede tener cualquier nombre)
        conn = sqlite3.connect('Users.db')

        # Retornamos la coneccion lograda
        return conn
    except Error:
        print(Error)
        sys.exit() # Cerramos el sistema

def login(conn, name, nickN, email, passw):
    """Ingresa un nuevo usuario a la base de datos"""

    cursor = conn.cursor() # creamos un cursor de la base de datos para realizar las consultas

    # cursor.execute() es el que genera cualquier consulta de sql en python, en este caso sera una consulta de insercion
    cursor.execute(" INSERT INTO Info_Usuario(Name, NickName, EmailAddres, Password) VALUES(:Name, :NickName, :EmailAddres, :Password, :LastName)",
                                        {'Name':name, 'NickName':nickN, # Las variables que no estan entre comillas simples son las que llevan los datos llegados a la funcion
                                        'EmailAddres':email, 'Password':passw}) # las que estan entre cmillas simples son las referenciadas en la consulta
    conn.commit() # conn.commit() guarda los cambios de las consultas en la base de datos

def Nick_existente(conn, nickN):
    """Verifica si un NickName ya existe"""

    cursor = conn.cursor() # creamos un cursor de la base de datos para realizar las consultas

    # Guardamos todos los resultados de registros en los que el nick del registro sean igual al nick mandado a la funcion
    resultados = cursor.execute(f" SELECT NickName FROM Info_Usuario WHERE NickName = '{nickN}'")

    # como los resultados de los registros se guardan en un diccionario lo controlamos con un for
    # este for recorre el diccionario registro por registro
    for resultado in resultados:
        # este for recorre un registro columna por columna
        for clave in resultado:
            # si el contenido de la comumna NickName de algun resultado es igual al nick mandado a la funcion ese nick existe y retornamos true
            if clave == nickN:
                return True

    # si llegamos aqui no existe el nick en los registros de la tabla asi que retornamos false
    return False

def correct_Sing_In(conn, password, nickN):
    """Verifica que los datos de un inicio de secion sean correctos"""

    cursor = conn.cursor() # creamos un cursor de la base de datos para realizar las consultas

    # Guardamos todos los resultados de registros en los que el nick del registro sean igual al nick mandado a la funcion
    # y la contraseña tambien es igual a la contraseña de la funcion
    resultados = cursor.execute(f" SELECT NickName, Password FROM Info_Usuario WHERE NickName = '{nickN}' AND Password = '{password}'")

    # en este caso como compararemos 2 atributos de la tabla usaremos 2 variables auxiliares para ver si los datos son correctos o no
    # por defecto estaran en false, y cambiaran si las encuentra
    Nick = False
    Pssw = False

    # como los resultados de los registros se guardan en un diccionario lo controlamos con un for
    # este for recorre el diccionario registro por registro
    for resultado in resultados:
        # este for recorre un registro columna por columna
        for clave in resultado:
            # si el contenido de la comumna NickName de algun resultado es igual al nick mandado a la funcion ese nick existe
            if clave == nickN:
                Nick = True
            # si el contenido de la comumna Password de algun resultado es igual a la contraseña mandado a la funcion esa contraseña esta correcta
            elif clave == password:
                Pssw = True

    # si ambos datos son correctos o existen retornamos true sino retornamos false
    if Nick == True and Pssw == True:
        return True
    else:
        return False
