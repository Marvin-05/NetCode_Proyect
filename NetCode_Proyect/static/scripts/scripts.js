const url = "https://ide-c71f377c0abd4ccaba7ed5c6be009bc1-8080.cs50.ws/temaSelected/0?";

function cargarContenido(){

    const httpx = new XMLHttpRequest();

    httpx.onload = function(){

        let datos = JSON.parse(this.responseText);

        let res = document.getElementById("tema");
        res.innerHTML = '';
        //console.log(datos);
        res.innerHTML += datos.Contenido;

    };

    httpx.open('Get', url);

    httpx.send();

}

function comentarios(){

    const httpx = new XMLHttpRequest();

    httpx.onload = function(){
        let datos = JSON.parse(this.responseText);

        let tabla = document.getElementById("tablaCuerpo");

        console.log(tabla)
        tabla.innerHTML = "";

        console.log(datos);
        for(let i = 0; i < datos.length; i++){

            tabla.innerHTML += '<tr> <td>' + datos[i].NickName + '</td> <td>' + datos[i].Comment + '<br> <a href="/eliminarComment/'+datos[i].Id+'" >ELIMINAR</a> </td> </tr>';

        }
    };

    httpx.open('GET', '/comentarios');
    httpx.send()

}

