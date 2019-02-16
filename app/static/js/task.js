function take_task(id){

$.ajax({
      url: '/take_task',
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