
//Ip textbox add-remove
var e = document.getElementById("option");
var ipText = document.getElementById("ipText");
function onChange() {
  var value = e.value;
  var text = e.options[e.selectedIndex].text;
  if (value == "Administrator") {
    document.getElementById("ipText").style.visibility = "hidden";
  } else {
    document.getElementById("ipText").style.visibility = "visible";
  }
}
e.onchange = onChange;
onChange();
