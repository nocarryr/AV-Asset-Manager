$(function(){
  var $scanDiv = $(".qrscanner");
  $scanDiv.html5_qrcode(function(data){
    console.log(data);
  }, function(readError){
    console.log('readError:', readError);
  }, function(videoError){
    console.log(videoError);
    $("body")
      .append('<h3>Could not open camera</h3>')
      .append('<p>' + videoError.name + '</p>')
      .append('<p>' + videoError.message + '</p>');
  });
});
