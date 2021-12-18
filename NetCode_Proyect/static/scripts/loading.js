$(window).on('load',function() {

    var contenedor = document.getElementById('jm-loadingpage');

    contenedor.style.visibility = 'hidden';
    contenedor.style.opacity = '0';
});
const navToggle = document.querySelector(".nav-palanca");
const navMenu = document.querySelector(".menu-responsive");

navToggle.addEventListener("click", () =>{
    navMenu.classList.toggle("nav-menu_visible");
    if(navMenu.classList.contains("nav-menu_visible")){
        navToggle.setAttribute("aria-label","Cerrar Menu");
    }else{
        navToggle.setAttribute("area-label","Abrir Menu");
    }
});