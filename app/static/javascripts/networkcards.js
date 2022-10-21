function eth0Status() {
  var eth0Status = document.getElementById("status").innerHTML;
  if (eth0Status.includes("Status:UP")) {
    console.log("eth0 up");
    try {
      document.getElementById("loading").remove();
    } catch {
      document.getElementById("eth0IntfContainer").style.borderColor = "green";
    }
  } else if (eth0Status.includes("Status:DOWN")) {
    console.log("eth0 down");
    try {
      document.getElementById("loading").remove();
    } catch {
      document.getElementById("eth0IntfContainer").style.borderColor = "red";
    }
  } else {
    console.log("eth0");
    document.getElementById("eth0IntfContainer").style.borderColor = "gray";
    document.getElementById("loading").style.visibility = "visible";
    document.getElementById("eth0Container").remove();
  }
}

function wlanStatus() {
  var a = document.getElementById("statuswlan").innerHTML;
  if (a.includes("Status:UP")) {
    try {
      document.getElementById("loading").remove();
    } catch {
      console.log("Dots removed");
    }
    document.getElementById("wlanIntfContainer").style.borderColor = "green";
  } else if (a.includes("Status:DOWN")) {
    try {
      document.getElementById("loading").remove();
    } catch {
      console.log("Dots removed");
    }
    document.getElementById("wlanIntfContainer").style.borderColor = "red";
  } else {
    document.getElementById("wlanIntfContainer").style.borderColor = "gray";
    document.getElementById("wlanContainer").remove();
  }
}
function gsmStatus() {
  var gsm = document.getElementById("gsmBand").innerHTML;
  if (
    gsm.includes("BAND:4") ||
    gsm.includes("BAND:3") ||
    gsm.includes("BAND:2")
  ) {
    try {
      document.getElementById("loading").remove();
    } catch {
      document.getElementById("gsmIntfContainer").style.borderColor = "green";
    }
  } else if (gsm.includes("BAND:-1")) {
    try {
      document.getElementById("loading").remove();
    } catch {
      document.getElementById("gsmIntfContainer").style.borderColor = "red";
    }
  } else {
    document.getElementById("gsmIntfContainer").style.borderColor = "gray";
    document.getElementById("loading").style.visibility = "visible";
  }
}
function eth1Status() {
  var eth1Status = document.getElementById("statusEth1").innerHTML;
  console.log(eth1Status);
  if (eth1Status.includes("Status:UP")) {
    try {
      document.getElementById("loading").remove();
    } catch {
      document.getElementById("eth1IntfContainer").style.borderColor = "green";
    }
  } else if (eth1Status.includes("Status:DOWN")) {
    try {
      document.getElementById("loading").remove();
    } catch {
      document.getElementById("eth1IntfContainer").style.borderColor = "red";
    }
  } else {
    document.getElementById("eth1IntfContainer").style.borderColor = "gray";
    document.getElementById("loading").style.visibility = "visible";
    document.getElementById("eth1Container").remove();
  }
}
