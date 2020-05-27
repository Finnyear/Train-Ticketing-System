var q_tickets_button = document.getElementById("q_tickets");
var q_transfer_button = document.getElementById("q_transfer");
var q_tickets_table = document.getElementById("q_tickets_t");
var json={ 
	orders:[{
			"trainID":'CHT',
			"d-station":'Shanghai', 
			"d-time":"12-21 13:23",
			"a-time":"12-21 13:23",
			"a_station":"Beijing",  
			"price":"100", 
			"seat":'50'
		}]
	};
var cnt_json = 0;
q_tickets_button.onclick=function(){
    q_tickets_t.style.display="block";
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
q_transfer_button.onclick=function(){
    q_tickets_t.style.display="block";
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
