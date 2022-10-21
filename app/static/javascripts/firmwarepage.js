const firmware = document.querySelector(".firmware");
const input = document.getElementById("file");
const Fbutton = document.getElementById("upload-buttonF");
const scss = document.createElement("p");

let timeout = async () => {
  await setTimeout(() => {
    scss.textContent = "";
    input.value = "";
  }, 5000);
};

input.onchange = function () {
  if (firmware.files[0].size / 1024 / 1024 < 3) {
    Fbutton.disabled = false;
    Fbutton.style.backgroundColor = "green";
    Fbutton.style.color = "white";
  } else {
    input.value = "";
    Fbutton.disabled = true;
    Fbutton.style.backgroundColor = "red";
    Fbutton.style.color = "white";
    alert("File size exceeds maximum limit! The core file must be max 2 Mb.");
  }
};
Fbutton.addEventListener("click", () => {
  if (input.files.length > 0) {
    scss.textContent = "Success!";
    document.getElementById("form").appendChild(scss);
    Pbutton.style.backgroundColor = "#d44a4a";
    timeout();
  }
});
