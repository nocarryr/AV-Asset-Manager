$(function(){
  var $scanDiv = $(".qrscanner"),
      $form = $(".qrscan-form");
  $scanDiv.html5_qrcode(function(data){
    $("#tagcode_input").val(data);
    $form.submit();
  }, function(readError){
    console.log('readError:', readError);
  }, function(videoError){
    console.log(videoError);
    $scanDiv
      .html5_qrcode_stop()
      .empty()
      .removeClass('qrscanner')
      .addClass('qrscan-item')
      .append('<h3>Could not open camera</h3>')
      .append('<p>' + videoError.name + '</p>')
      .append('<p>' + videoError.message + '</p>')
      .delay(1500)
      .slideUp(800);
    $("p:empty", $scanDiv).remove();
    $(".qrscan-buttonset").hide();
    $form.show();
    $("#tagcode_input").focus();
  });
  $("#stop-btn").click(function(e){
    e.preventDefault();
    $scanDiv.html5_qrcode_stop();
  });
  $("#form-open-btn").click(function(e){
    e.preventDefault();
    $scanDiv.html5_qrcode_stop();
    $scanDiv.hide();
    $(".qrscan-buttonset").hide();
    $form.show();
    $("#tagcode_input").focus();
  });
});
