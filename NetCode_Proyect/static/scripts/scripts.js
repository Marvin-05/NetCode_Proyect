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