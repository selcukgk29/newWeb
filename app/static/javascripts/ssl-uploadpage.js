const input = document.getElementById("sslPage");
const sslUploadButton = document.getElementById("sslUploadButton");


input.onchange = function () {
  if (input.files[0].size / 1024 / 1024 < 5) {
    sslUploadButton.disabled = false;
    sslUploadButton= "green";
    sslUploadButton = "white";
  } else {
    input.value = "";
    sslUploadButton.disabled = true;
    sslUploadButton.style.backgroundColor = "red";
    sslUploadButton.style.color = "white";
    alert(
      "File size exceeds maximum limit! The project file must be max 5 Mb."
    );
  }
};
