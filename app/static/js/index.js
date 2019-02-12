function switch_content(id,hide_id,show_id,class_remove, class_replace){

let vhide = document.getElementById(hide_id).style["display"]="none";
let vshow = document.getElementById(show_id).style["display"]="block";
let element = document.getElementById(id)
element.classList.remove(class_remove)
element.classList.add(class_replace);
element.setAttribute("onclick", `switch_content('${id}','${show_id}','${hide_id}','${class_replace}' ,'${class_remove}')`);


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
	new_element.classList.add('tag-element');
	new_element.innerHTML=i.id
	tageditor.appendChild(new_element)
	tageditor.insertBefore(new_element, tageditor.childNodes[0]);

	
	str_of_tags=str_of_tags.concat(i.id+=";")



}

}
console.log(str_of_tags)
element_tag.setAttribute("style", "width:300px;")


}