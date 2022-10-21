var portPattern =
  /\b(65[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\:(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/;
$(".port")
  .keypress(function (e) {
    if (
      e.which != 8 &&
      e.which != 0 &&
      e.which != x &&
      (e.which < 47 || e.which > 58)
    ) {
      console.log(e.which);
      return false;
    }
  })
  .keyup(function () {
    var this1 = $(this);
    var port = this1.val();
    console.log(port.search(":"));

    if (port.search(":") == -1) {
      if (port) {
        $(this).css({
          border: " 2px solid #ccc",
          "border-radius": " 4px",
        });
      }
    } else {
      var port = this1.val().split(":");
      console.log(port);
      if (port[1] > port[0]) {
        $(this).css({
          border: " 2px solid #ccc",
          "border-radius": " 4px",
        });
      } else {
        $(this).css({
          border: " 2px solid #D81E5B",
          "border-radius": " 4px",
        });
      }
    }
  });

var pattern =
  /\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/;
x = 20;
$(".ipInput")
  .keypress(function (e) {
    if (
      e.which != 8 &&
      e.which != 0 &&
      e.which != x &&
      (e.which < 47 || e.which > 58)
    ) {
      console.log(e.which);
      return false;
    }
  })
  .keyup(function () {
    var this1 = $(this);
    if (!pattern.test(this1.val())) {
      console.log("Not valid");
      $(this).css({
        border: "solid 3px #D81E5B",
        outline: "none",
        "border-radius": " 4px",
      });
      while (this1.val().indexOf("..") !== -1) {
        this1.val(this1.val().replace("..", "."));
      }
      x = 46;
    } else {
      x = 0;
      var lastChar = this1.val().substr(this1.val().length - 1);
      if (lastChar == ".") {
        this1.val(this1.val().slice(0, -1));
      }
      var ip = this1.val().split(".");
      if (ip.length == 4) {
        $(this).css({
          border: " 2px solid #ccc",
          "border-radius": " 4px",
        });
      }
    }
  });
