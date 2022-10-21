var e = document.getElementById("option");
var destinationPort = document.getElementById("destinationPort");
var sourcePort = document.getElementById("sourcePort");
var afterElement = document.getElementById("afterElement");
var sourceAdress = document.getElementById("sourceAddress");
function onChange() {
  var value = e.value;
  var text = e.options[e.selectedIndex].text;
  if (text == "ICMP" || text == "ALL" || text == "SNAT") {
    destinationPort.remove();
    sourcePort.remove();
    document.getElementById("destInput").required = true;
    document.getElementById("sourceId").required = true;
  } else {
    afterElement.after(destinationPort);
    sourceAdress.after(sourcePort);
  }
}
e.onchange = onChange;
onChange();
