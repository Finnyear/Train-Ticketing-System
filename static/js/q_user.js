var q_user_button = document.getElementById("q_user");
var q_user_table = document.getElementById("q_user_t");
var m_input_ = document.getElementById("m_input");
var q_td = q_user_table.getElementsByTagName("td");
var m_inputs = m_input_.getElementsByTagName("input");
var json={username:'CHT', name:'cht', mail:'cht@163.com', p:5};
var cnt_json = 0;
q_user_button.onclick=function(){
    q_user_t.style.display="block";
    for(var i in json){
    	q_td[cnt_json].innerHTML = json[i];
    	cnt_json++;
    }
    cnt_json = 0;
}

var modify_button = document.getElementById("m_user");
var warning_page_button = document.getElementById("warning_page");
var warning_button = document.getElementById("warning");
var cancel_button = document.getElementById("cancel");
modify_button.onclick=function(){
    warning_page_button.style.display="inline";
    warning_button.style.display="inline";
}
cnt_json = 0;
for(var i in json){
    	m_inputs[cnt_json].value = json[i];
    	cnt_json++;
    }
cnt_json = 0;
cancel_button.onclick=function(){
    warning_page_button.style.display="none";
    warning_button.style.display="none";
}