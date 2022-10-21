$(document).ready(function () {
  var status = $("#statusSpan").text();
  var wlanStatus = $("#wlanState").text();
  console.log(wlanStatus[1]);
  if (wlanStatus[1] == "2") {
    $("#disableButton").css("background-color", "#E0144C");
  } else {
    $("#disableButton").css("background-color", "gray");
  }
  if (wlanStatus[1] == "1") {
    $("#hotspotButton").css("background-color", "#B6E388");
  } else {
    $("#hotspotButton").css("background-color", "gray");
  }
  if (wlanStatus[1] == "0") {
    $("#clientButton").css("background-color", "#B6E388");
  } else {
    $("#clientButton").css("background-color", "gray");
  }

  $("#disableButton").click(function () {
    $("input").prop("disabled", true);
    $.post("/en/ipSettings/wlan/disable", function (data) {
      $("#disableButton").css("background-color", "#E0144C");
      $("#clientButton").css("background-color", "gray");
      $("#hotspotButton").css("background-color", "gray");
    });
  });
  $("#hotspotButton").click(function () {
    $("input").prop("disabled", false);
    $("#disableButton").css("background-color", "gray");
    $("#clientButton").css("background-color", "gray");
    $("#hotspotButton").css("background-color", "#B6E388");
    if (status === "Status") {
      window.location.href = "/en/ipSettings/wlan/hotspot";
    } else {
      window.location.href = "/tr/ipAyarlari/wlan/hotspot";
    }
  });
  $("#clientButton").click(function () {
    $("input").prop("disabled", false);
    $("#disableButton").css("background-color", "gray");
    $("#clientButton").css("background-color", "#B6E388");
    $("#hotspotButton").css("background-color", "gray");
    if (status === "Status") {
      window.location.href = "/en/ipSettings/wlan";
    } else {
      window.location.href = "/tr/ipAyarlari/wlan";
    }
  });
});
