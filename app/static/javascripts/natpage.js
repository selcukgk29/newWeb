var e = document.getElementById("option");
var toSource = document.getElementById("destinationPort");
var afterElement = document.getElementById("afterElement");
function onChange() {
  var text = e.options[e.selectedIndex].text;
  if (text == "MASQUERADE") {
    toSource.remove();
  } else {
    afterElement.after(toSource);
  }
}
e.onchange = onChange;
onChange();
