function switch_content(id,hide_id,show_id,class_remove, class_replace){

let vhide = document.getElementById(hide_id).style["display"]="none";
let vshow = document.getElementById(show_id).style["display"]="block";
let element = document.getElementById(id)
element.classList.remove(class_remove)
element.classList.add(class_replace);
element.setAttribute("onclick", `switch_content('${id}','${show_id}','${hide_id}','${class_replace}' ,'${class_remove}')`);


}
