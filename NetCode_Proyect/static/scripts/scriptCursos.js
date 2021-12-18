window.addEventListener("load", e => {
    const forms = document.querySelectorAll(".btn_tema");

    forms.forEach(form => {
        form.addEventListener("submit", e => {
             e.preventDefault();

             console.log(e.target.action);

             const httpx = new XMLHttpRequest();

             httpx.onload = function(){

                 let datos = JSON.parse(this.responseText);

                 let res = document.getElementById("tema");
                 res.innerHTML = '';
                 //console.log(datos);
                 res.innerHTML += datos.Contenido;

             };

             httpx.open('Get', e.target.action);

             httpx.send();

        });
    });
});