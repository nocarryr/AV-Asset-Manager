$(function(){
  var $scanDiv = $(".qrscanner");
  $scanDiv.html5_qrcode(function(data){
    var url = $scanDiv.data('resulturl') + data;
    window.location = url;
  }, function(readError){
    console.log('readError:', readError);
  }, function(videoError){
    console.log(videoError);
    $("body")
      .append('<h3>Could not open camera</h3>')
      .append('<p>' + videoError.name + '</p>')
      .append('<p>' + videoError.message + '</p>');
  });
  $("#stop-btn").click(function(e){
    e.preventDefault();
    $scanDiv.html5_qrcode_stop();
  });
});
