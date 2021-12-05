
$("#C_0").click(function(){

   $.ajax({

      url : "cursoC.html",

      succes : function(data){
         $("#tema").html(data)
      }

   });

});