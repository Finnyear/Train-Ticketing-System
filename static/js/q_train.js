var q_train_button = document.getElementById("q_train");
var q_train_table = document.getElementById("q_train_t");
var q_span = q_train_table.getElementsByTagName("span");
var json={
	trainid:'CHT', 
	type:'G', 
	stations:[{
			"s_name":'Shanghai', 
			"a_time":"-", 
			"d-time":"12-21 13:23", 
			"price":"100", 
			"r_ticket":'50'
		},{
			"s_name":'Nanjing', 
			"a_time":"12-22 14:23", 
			"d-time":"12-21 17:53", 
			"price":"100", 
			"r_ticket":'50'
		},{
			"s_name":'Beijing', 
			"a_time":"12-25 1:41", 
			"d-time":"-", 
			"price":"100", 
			"r_ticket":'-'
		}]
	};
var cnt_json = 0;
q_train_button.onclick=function(){
    q_train_t.style.display="block";
    q_span[0].innerHTML = json['trainid'];
    q_span[1].innerHTML = json['type'];
    for(var i in json['stations']){
    	cnt_json++;
    	var tmp_tr = document.createElement('tr');
    	var tmp_th = document.createElement('th');
    	tmp_th.innerHTML = cnt_json;
    	tmp_tr.appendChild(tmp_th);
    	for (var j in json['stations'][i]){
    		var tmp_td = document.createElement('td');
    		tmp_td.innerHTML = json['stations'][i][j];
    		tmp_td.style = "text-align:center";
    		tmp_tr.appendChild(tmp_td);
    	}
    	tmp_tr.scope="row";
    	t_body.appendChild(tmp_tr);
    }
    cnt_json = 0;
}