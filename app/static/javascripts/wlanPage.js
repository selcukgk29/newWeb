var inputs = document.getElementsByTagName("INPUT");
var applybutton = document.getElementById("applyWLAN");

function active() {
  for (var i = 0; i < inputs.length; i++) {
    if (inputs[i].type === "text") {
      inputs[i].disabled = false;
      applybutton.disabled = false;
    }
  }
}
function deactive() {
    console.log("burada");
  for (var i = 0; i < inputs.length; i++) {
    if (inputs[i].type === "text") {
      inputs[i].disabled = true;
      inputs[i].value = "";
      applybutton.disabled = true;
    }
  }
}
