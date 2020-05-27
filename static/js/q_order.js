var q_order_button = document.getElementById("q_order");
var q_order_table = document.getElementById("q_order_t");
var json={ 
	orders:[{
			"status":'IS PENDING',
			"trainID":'CHT',
			"d-station":'Shanghai', 
			"d-time":"12-21 13:23",
			"a-time":"12-21 13:23",
			"a_station":"Beijing",  
			"price":"100", 
			"r_ticket":'50'
		}]
	};
var cnt_json = 0;
q_order_button.onclick=function(){
    q_order_t.style.display="block";
    for(var i in json['orders']){
    	cnt_json++;
    	var tmp_tr = document.createElement('tr');
    	var tmp_th = document.createElement('th');
    	tmp_th.innerHTML = cnt_json;
    	tmp_tr.appendChild(tmp_th);
    	for (var j in json['orders'][i]){
    		var tmp_td = document.createElement('td');
    		tmp_td.innerHTML = json['orders'][i][j];
    		tmp_td.style = "text-align:center";
    		tmp_tr.appendChild(tmp_td);
    	}
    	tmp_tr.scope="row";
    	t_body.appendChild(tmp_tr);
    }
    cnt_json = 0;
}