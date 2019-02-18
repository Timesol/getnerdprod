function remove_task(id){

$.ajax({
      url: '/remove_task',
                        type: "POST",
      data: { id:id ,},
    
      success: function(response){
        console.log(response);
        
      },
      error: function(error){
        console.log(error);
      }
    });

}


function close_task(id){

$.ajax({
      url: '/close_task',
                        type: "POST",
      data: { id:id ,},
    
      success: function(response){
        console.log(response);
        
      },
      error: function(error){
        console.log(error);
      }
    });

}

$(document).ready(function(){
refresh('/tasks_taken_r','container-taken-tasks')
refresh('/tasks_created_r','container-created-tasks')

 }); 



function refresh(url,container){

  var xhttp;
  if (window.XMLHttpRequest) {
    // code for modern browsers
    xhttp = new XMLHttpRequest();
    
    } else {
    // code for IE6, IE5
    xhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById(container).innerHTML = this.responseText;
      
      
    }
  };

  xhttp.open("GET" , url, true);
  
  xhttp.send();
 

}



