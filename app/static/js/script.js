$(document).ready(function(){

  //Set up a 'current number variables'
  var current_number = '';
  var contact_dict = {};
  var last_click = $('thead');
 
  get_update_contact();
  //On clicking an entry from the contact board
  $('tbody').children().click(function(){
  	if ($('tbody').children() != last_click){
  	    last_click = $('tbody').children(); //avoid pulling data from server again
  	    current_number = $(this).find('td.phone').text();
  	    get_update_message(current_number, 0);
  	}
  });
  
  $('#send-button').click(send_message(current_number));
})

/* Comment:
1. Overall structure: get_update_contact() -> get_update_dict() -> get_update_messages.
2. Rendering happens in get_update_dict() for the contact board, and in get_update_messages for the message board. Heartbeat only happens in get_update_contact(). 
3. On clicking onto another contact entry, call get_update_messages with counts = 0*/

//If get_update_contact() shows there's an update the selected number, we will send a request to update the message board for this number.
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
        
        }
    });
}

function get_update_contact(){
    setTimeout(get_update_contact, 1000);
    $.ajax({
    	type: 'GET',
    	url: '/api/contact_updates',
    	success: function(json){ //json contains a contact_num dictionary
    	    //$('#conversation').before('<p style="color:blue">'+'<strong>I said:</strong> '+'succeed'+'</p>');
    	}
    });
}


//Just update the number of messages associated with every number in contact dict
function update_contact_dict(contact_dict, server_dict,current_number){
    //Check current number
    if (contact_dict[current_number] < server_dict[current_number]){
        //dispatch get_update_messages to update the message board for the current number under admin's selection
        get_update_messages(current_number, contact_dict[current_number]);
    }
    for (phone_number in server_dict){
    	if (contact_dict[phone_number] != server_dict[phone_number]){
    	    if (contact_dict[phone_number] == null){
    	        //Todo: render html
    	        
    	    }
    	    else{
    	        //Todo: just highlight the background
    	    }
    	}
        contact_dict[phone_number] = server_dict[phone_number];
    }
}

function send_message(phone_number){ //or facebook id
    var toAdd = $('#inputbox').val();
    $('#conversation').before('<p style="color:blue">'+'<strong>I said:</strong> '+toAdd+'</p>');
    $('#inputbox').val('');
    var msg = {
    	number: "0",
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
}

