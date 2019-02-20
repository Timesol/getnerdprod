function load_task(id){

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
       document.getElementById("Container-Index-Main-Content").style["display"]="none";
       document.getElementById("Container-Index-Add-Task").style["display"]="none";
       document.getElementById("container-user").style["display"]="none"; 
       document.getElementById("container-task").innerHTML=this.responseText;
       document.getElementById("container-task").style["display"]="block";

      this.responseText;
      
      
    }
  };

  xhttp.open("GET", '/task/'+id,  true);
  
  xhttp.send();
 

}






function switch_content(id,hide_id,hide_id2,hide_id3,show_id,class_remove, class_replace){

let vhide = document.getElementById(hide_id).style["display"]="none";
let vhide2 = document.getElementById(hide_id2).style["display"]="none";
let vhide3 = document.getElementById(hide_id3).style["display"]="none";
let vshow = document.getElementById(show_id).style["display"]="block";
let element = document.getElementById(id)
element.classList.remove(class_remove)
element.classList.add(class_replace);
element.setAttribute("onclick", `switch_content("${id}","${show_id}","${hide_id3}","${hide_id2}","${hide_id}","${class_replace}" ,"${class_remove}")`);


}


function select_categorys(){


let element = document.getElementsByClassName("checked-data");
let element_tag=document.getElementById("tags")
let tageditor=document.getElementById("tag-editor")
let tagform=document.getElementById("tag-form")
let str_of_tags=""
for (let i of element){
	
if (i.checked == true){
	let new_element=document.createElement("SPAN")
	let deletetag=document.createElement("A")
	deletetag.setAttribute("onclick", `delete_tag("${i.id}")`)
	deletetag.innerHTML="&times;";
	new_element.classList.add("tag-element");
	new_element.innerHTML=i.id+" "
	new_element.id=i.id
	deletetag.classList.add("deltag")


	tageditor.appendChild(new_element)
	new_element.appendChild(deletetag)
	tageditor.insertBefore(new_element, tageditor.childNodes[0]);

	
	



}

}
console.log(str_of_tags)
element_tag.setAttribute("style", "width:300px;")


}

$(document).ready(function(){

$("#select-tag-b").click(function() {


 $("#modal-tags1").modal("hide");



});
});


function delete_tag(id){

let element = document.getElementById(id);
element.parentNode.removeChild(element);






}

$(document).ready(function(){
	
   


let form = document.getElementById("form-async");
let input= document.getElementById("file-input");
let slideshow_container= document.getElementById("slideshow-container")
let img_container=document.getElementById("img-upload-container");


form.onchange= function(ev) {
  
  let new_element=document.createElement("IMG");
  let flex_item=document.createElement("DIV");
  let uploaded_img=document.createElement("IMG");



 


  
  
  
  let oData = new FormData(form);
  let oReq = new XMLHttpRequest();
  oReq.open("POST", "asynch_file", true);
  oReq.onload = function(oEvent) {
    if (oReq.status == 200) {


      flex_item.setAttribute("class", "flex-item ")
      img_container.insertBefore(flex_item, img_container.childNodes[0]);
      uploaded_img.setAttribute("src", JSON.parse(oReq.responseText).result_image_location);
      uploaded_img.setAttribute("class","new_pics");
      flex_item.appendChild(uploaded_img);
       

    } else {
      alert("Error " + oReq.status + " occurred when trying to upload your file")
    }






  };
  oReq.send(oData);
  ev.preventDefault();
};


});



function take_task(id){

$.ajax({
      url: '/take_task',
                        type: "POST",
      data: { id:id ,},
    
      success: function(response){
        console.log(response);
        data=JSON.parse(response);
        if (data.message){
        let element=document.getElementById('errors_message')
        element.innerHTML=data.message;
        element.style["display"]="block";
        setTimeout(function() {


          element.style["display"]="none";

        }, 3000);

       }
        
      },
      error: function(error){
        console.log(error);
      }
    });

}

function load_content(){
setTimeout(function() {
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


}, 1000);


}




var slideIndex = 1;
showDivs(slideIndex);

function plusDivs(n) {
  showDivs(slideIndex += n);
}

function showDivs(n) {
  var i;
  var x = document.getElementsByClassName("taskimg-flexcontainer");
  if (n > x.length) {slideIndex = 1}
  if (n < 1) {slideIndex = x.length} ;
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  x[slideIndex-1].style.display = "flex";
}
