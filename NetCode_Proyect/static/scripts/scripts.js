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