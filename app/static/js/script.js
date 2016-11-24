$(document).ready(function(){

  //Set up a 'current number variables'
  var current_number = '124';
  var contact_dict = {};
 
  get_update_contact(contact_dict, current_number);
  //On clicking an entry from the contact board
  $('tbody').children().click(function(){
  	//$('tbody').children().css("background-color", default);
  	if (current_number != $(this).find('td.phone').text()){
  	    alert("not same");
  	    $('p').remove();
  	    last_click = $('tbody').children(); //avoid pulling data from server again
  	    current_number = $(this).find('td.phone').text();
  	    get_update_message(current_number, 0);
  	}
  });
  
  $('#send-button').click(function(){
    var toAdd = $('#inputbox').val();
    //alert("click");
    $('#conversation').before('<p class="dialog" style="color:blue">'+'<strong>Admin said:</strong> '+toAdd+'</p>');
    $('#inputbox').val('');
    var msg = {
    	number: current_number,
    	content: "FROM ME: "+toAdd,
    	//type = sms || fb
    	type: "sms",
    }
    $.ajax({
    	type: 'POST',
    	url: '/api/sms_post',
    	data: msg,
    	success:function(json){
    	    alert(json.result);
    	}
    });
  });
})

/* Comment:
1. Overall structure: get_update_contact() -> get_update_dict() -> get_update_messages.
2. Rendering happens in get_update_dict() for the contact board, and in get_update_messages for the message board. Heartbeat only happens in get_update_contact(). 
3. On clicking onto another contact entry, call get_update_messages with counts = 0*/

//If get_update_contact() shows there's an update for the selected number, we will send a request to update the message board for this number.
function get_update_message(phone_number, counts){ //Todo: or fb_id
    var info = {
        number: phone_number,
        count: counts,
    }
    $.ajax({
        type: 'GET',
        url: 'api/message_updates',
        data: info,
        success: function(json){ /*The only job here is to render the message board*/
            var msg_entry;
            for (msg_entry in json.new_message_list){
            	$('#conversation').before('<p style="color:blue">'+msg_entry+'</p>');
            }
        }
    });
}

function get_update_contact(contact_dict, current_number){
    setTimeout(get_update_contact, 1000);
    $.ajax({
    	type: 'GET',
    	url: '/api/contact_updates',
    	success: function(json){ //json contains a contact_num dictionary
    	//refer to def send_contact_update(): from the flask back-end
    	    var server_dict = json.contact_list; 
    	    if (server_dict != undefined){
    	   	 update_contact_dict(contact_dict, server_dict, current_number);
    	    }
    	}
    });
}


//Just update the number of messages associated with every number in contact dict
function update_contact_dict(contact_dict, server_dict,current_number){
    //Check current number
    if (contact_dict[current_number] == undefined){
    	contact_dict[current_number] = server_dict[current_number];
    	get_update_message(current_number, contact_dict[current_number]);
    }
    else if (contact_dict[current_number] < server_dict[current_number]){
        //dispatch get_update_messages to update the message board for the current number under admin's selection
        get_update_message(current_number, contact_dict[current_number]);
    }
    for (phone_number in server_dict){
    	if (contact_dict[phone_number] != server_dict[phone_number]){
    	    if (contact_dict[phone_number] == null){
    	        //Todo: render html
    	        alert("to_add");
    	        $('tr#bot').before(
    	          '<tr class="contact" id=' + phone_number + '>'+
    	          //Todo: to populate the name & location later
      	          '<td class="name">' + 'unknown(name)' + '</td>' +
      	          '<td class="count">' + server_dict[phone_number] + '</td>' +
      	          '<td class="phone">' + phone_number + '</td>' +
      	          '<td class="location">' +'unknown(location)' + '</td>' +
      	          '</tr>'
    	        );
    	    }
    	    else{
    	        //Todo: just highlight the background
    	       // $('tr#'+ phone_number).css(background-color: #bcd6ff);
    	    }
    	}
        contact_dict[phone_number] = server_dict[phone_number];
    }
}

