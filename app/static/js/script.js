$(document).ready(function(){

  //just a test here
  polling();
  $('#send-button').click(function(){
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
  });
})

function populate_contact(data){

}

function polling(){
    setTimeout(polling, 1000);
    $.ajax({
    	type: 'GET',
    	url: '/api/contact_updates',
    	success: function(data){
    	    //$('#conversation').before('<p style="color:blue">'+'<strong>I said:</strong> '+'succeed'+'</p>');
    	}
    });
}

function retrieve_history(number){
    $.ajax({
    	type: 'GET',
    	url: /api/message_history,
    	data: number,
    	success: function(json){
    	
    	}
    });
}


