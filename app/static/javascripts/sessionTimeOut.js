var counter = 60;
var idleTime = 0;
var countdown;
$(document).ready(function () {
  $(window).click(function () {
    console.log("click has occured");
    idleTime = 0;
  });

  $(window).keyup(function () {
    console.log("key up has occured");
    idleTime = 0;
  });

  //Increment the idle time counter every minute.
  var idleInterval = setInterval(timerIncrement, 60000); //found
  $("#keep").click(function () {
    idleTime = 0;
    $("#timeOutWarningOverlay").hide();
    clearInterval(idleInterval);
  });
});
function timerIncrement() {
  idleTime = idleTime + 1;
  console.log(idleTime);
  if (idleTime > 13) {
    //13
    $("#timeOutWarningOverlay").show();
    startTimer();
  }
  if (idleTime > 14) {
    // 14
    setTimeout(function () {
      window.location.href = "/";
    }, 60000);
  }
}
function startTimer() {
  countdown = setInterval(countDownClock, 1000);
}

function countDownClock() {
  counter = counter - 1;
  if (counter < 10) {
    console.log(counter);
    $("#time").text("0" + counter);
  } else {
    console.log(counter);
    $("#time").text(counter);
  }
  if (counter == 0) {
    counter = 60;
    $("#timeOutWarningOverlay").hide();
    clearInterval(countdown);
    console.log("done");
  }
}
