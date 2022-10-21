const input = document.getElementById("projectfile");
const Pbutton = document.getElementById("upload-buttonP");
const scss = document.createElement("p");

let timeout = async () => {
  await setTimeout(() => {
    scss.textContent = "";
    input.value = "";
  }, 5000);
};
input.onchange = function () {
  if (input.files[0].size / 1024 / 1024 < 5) {
    Pbutton.disabled = false;
    Pbutton.style.backgroundColor = "green";
    Pbutton.style.color = "white";
  } else {
    input.value = "";
    Pbutton.disabled = true;
    Pbutton.style.backgroundColor = "red";
    Pbutton.style.color = "white";
    alert(
      "File size exceeds maximum limit! The project file must be max 5 Mb."
    );
  }
};

Pbutton.addEventListener("click", () => {
  if (input.files.length > 0) {
    scss.textContent = "Success!";
    document.getElementById("form").appendChild(scss);
    Pbutton.style.backgroundColor = "#d44a4a";
    timeout();
  }
});
