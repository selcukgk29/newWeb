var myButton = document.getElementsByName("dynamic");
var myInput = document.getElementsByName("newUserPassword");
myButton.forEach(function (element, index) {
  element.onclick = function () {
    "use strict";
    if (myInput[index].type == "password") {
      myInput[index].setAttribute("type", "text");
    } else {
      myInput[index].setAttribute("type", "password");
    }
  };
});

//Show hide password icon
