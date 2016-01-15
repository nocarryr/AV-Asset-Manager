$(function(){
  var $scanDiv = $(".qrscanner"),
      $form = $(".qrscan-form");
  var buildUrl = function(tagcode){
    return $scanDiv.data('resulturl') + tagcode;
  };

  $scanDiv.html5_qrcode(function(data){
    window.location = buildUrl(data);
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
  $form.submit(function(e){
    var tagcode = $("#tagcode_input").val();
    $form.attr('action', buildUrl(tagcode));
  })
});
