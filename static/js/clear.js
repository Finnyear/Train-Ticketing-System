var clear_button = document.getElementById("clear");
var warning_page_button = document.getElementById("warning_page");
var warning_button = document.getElementById("warning");
var cancel_button = document.getElementById("cancel");
clear_button.onclick=function(){
    warning_page_button.style.display="inline";
    warning_button.style.display="inline";
}
cancel_button.onclick=function(){
    warning_page_button.style.display="none";
    warning_button.style.display="none";
}