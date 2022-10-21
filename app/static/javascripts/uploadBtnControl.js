const input = document.getElementById("file");
const button = document.getElementById("upload-button");
const scss = document.createElement("p");

let timeout = async () => {
  console.log("intervalF fonks");
  await setTimeout(() => {
    scss.textContent = "";
    input.value = "";
    console.log("await fonks");
  }, 5000);
};
input.onchange = function () {
  const file = this.files;
  if (file.length > 0) {
    button.disabled = false;
    button.style.backgroundColor = "green";
    button.style.color = "white";
    console.log("yüklendi");
    clearTimeouts();
  }
};
button.addEventListener("click", () => {
  if (input.files.length > 0) {
    scss.textContent = "Success!";
    document.getElementById("form").appendChild(scss);
    button.style.backgroundColor = "#d44a4a";
  }
  timeout();
});


