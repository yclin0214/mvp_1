$(document).ready(function(){
  $('#send-button').click(function(){
    var toAdd = $('#inputbox').val();
    $('#conversation').before('<p style="color:blue">'+'<strong>I said:</strong> '+toAdd+'</p>');
    $('#inputbox').val('');
  });
})

