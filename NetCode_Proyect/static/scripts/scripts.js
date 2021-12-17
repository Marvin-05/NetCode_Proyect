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

/*
function cargarContenido(){
    let parameters = {
    };

    let nTema = 0;

    let url = "/temaSelected/"+nTema

    // obtenemos los articulos buscados en articles segun geo
    $.getJSON(url, parameters, function(data, txtStatus, jqXHR){

        let res = document.getElementById("tema");
        res.innerHTML = '';
        console.log(data);
        res.innerHTML += data[0].Contenido;

    });
}



function Content(id, c_id){


    const httpx = new XMLHttpRequest();

    httpx.open('Get', "Temas.json", true);

    httpx.send();

    httpx.onreadystatechange = function(){

        if (this.readyState == 4 && this.status == 200){

            let datos = JSON.parse(this.responseText);

            let res = document.querySelector("#tema");
            res.innerHTML = '';

            res.innerHTML += datos[id].Contenido;
        }

    };
}
*/

