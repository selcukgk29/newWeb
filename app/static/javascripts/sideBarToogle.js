//Side bar toogle button
document.getElementById("sidebarToggle").addEventListener("click", () => {
  if (document.getElementById("accordionSidebar").style.display == "none") {
    document.getElementById("accordionSidebar").style.display = "flex";
    document.getElementById("midImg").style.visibility = "hidden";
  } else {
    document.getElementById("accordionSidebar").style.display = "none";
    document.getElementById("midImg").style.visibility = "visible";
  }
});
