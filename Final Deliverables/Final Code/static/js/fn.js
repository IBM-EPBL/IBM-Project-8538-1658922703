$(function () {
  $("#in_image").change(function () {
    $("#preview").html("");
    var regex = /^([a-zA-Z0-9\s_\\.\-:])+(.jpg|.jpeg|.gif|.png|.bmp)$/;
    if (regex.test($(this).val().toLowerCase())) {
      if ($.browser.msie && parseFloat(jQuery.browser.version) <= 9.0) {
        $("#preview").show();
        $("#preview")[0].filters.item(
          "DXImageTransform.Microsoft.AlphaImageLoader"
        ).src = $(this).val();
      } else {
        if (typeof FileReader != "undefined") {
          $("#preview").show();
          $("#preview").append("<img />");
          var reader = new FileReader();
          reader.onload = function (e) {
            $("#preview img").attr("src", e.target.result);
            $("#remove").show();
          };
          reader.readAsDataURL($(this)[0].files[0]);
        } else {
          alert("This browser does not support FileReader.");
        }
      }
    } else {
      alert("Please upload a valid image file.");
    }
  });
});

$("#remove").on("click", () => {
  document.getElementById("img_form").reset();
  $("#preview").hide();
  $("#remove").hide();
  clean_res();
});

$("#img_form").on("submit", function (ev) {
  document.getElementById("sub").value = "Please Wait....";
  ev.preventDefault();
  var formData = new FormData(this);
  $.ajax({
    url: "/recog",
    type: "POST",
    data: formData,
    success: (val) => build_res(val),
    cache: false,
    contentType: false,
    processData: false,
  });
});

function clean_res() {
  document.getElementById("res_box").innerHTML = "";
}

function build_res(val) {
  var resBox = document.getElementById("res_box");

  if (val != "Invalid Input") {
    var span = document.createElement("SPAN");
    span.setAttribute("id", "result");
    span.innerHTML = "Digit: "+val ['num']+"<br>Probability: "+val['prob']+"%";
    resBox.appendChild(span);
  } else {
    resBox.innerHTML = val;
  }
  document.getElementById("sub").value = "Recognize";
}
