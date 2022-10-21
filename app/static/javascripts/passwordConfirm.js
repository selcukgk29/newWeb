var check = function () {
  if (
    document.getElementById("show_hide_password").value ==
      document.getElementById("confirm_password").value &&
    document.getElementById("show_hide_password").value.length > 6 &&
    document.getElementById("show_hide_password").value.length < 12
  ) {
    document
      .getElementById("show_hide_password")
      .setAttribute("style", "border:solid 3px #1cc88a");
    document
      .getElementById("confirm_password")
      .setAttribute("style", "border:solid 3px #1cc88a");
    document.getElementById("apply").removeAttribute("disabled");
  } else {
    document
      .getElementById("show_hide_password")
      .setAttribute("style", "border:solid 3px #e74a3b");
    document
      .getElementById("confirm_password")
      .setAttribute("style", "border:solid 3px #e74a3b");
    document.getElementById("apply").setAttribute("disabled", "disabled");
  }
};
