




function switch_content(id,hide_id,show_id,class_remove, class_replace){

let vhide = document.getElementById(hide_id).style["display"]="none";
let vshow = document.getElementById(show_id).style["display"]="block";
let element = document.getElementById(id)
element.classList.remove(class_remove)
element.classList.add(class_replace);
element.setAttribute("onclick", `switch_content("${id}","${show_id}","${hide_id}","${class_replace}" ,"${class_remove}")`);


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



