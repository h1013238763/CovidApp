index = 1;
const panel_list = [
  "sign_in_panel",
  "register_panel",
  "forget_password_panel",
  "reset_password_panel",
];

// Sign Page Image Change Functions
function ChangeImage() {
  var div = document.getElementById("image_button_panel");
  var baseUrl = div.getAttribute("data-url");
  var image = document.getElementById("show_image");

  image.style.opacity = 0;
  setTimeout(function () {
    image.src = baseUrl + index + ".jpg";
    image.style.opacity = 1;
  }, 800);

  var button = document.getElementById("image_button_" + index);
  button.style.width = 45;

  other_index = index;
  for (i = 0; i < 2; i++) {
    other_index++;
    if (other_index > 3) {
      other_index = 1;
    }
    document.getElementById("image_button_" + other_index).style.width = 20;
  }
}
function ChangeImageIndex(image_index) {
  index = image_index;
  ChangeImage();
}
function ChangeIndex() {
  index++;
  if (index > 3) {
    index = 1;
  }
  ChangeImage();
}
var image_change_interval = setInterval(ChangeIndex, 10000);

// Panel Switch Functions
function SwitchPanel(panel_index) {
  for (i = 0; i < panel_list.length; i++) {
    if (i == panel_index) {
      console.log(panel_list[i] + " active");
      document.getElementById(panel_list[i]).style.display = "grid";
    } else {
      console.log(panel_list[i] + " deactive");
      var component = document.getElementById(panel_list[panel_index]);
      console.log(component);
      document.getElementById(panel_list[i]).style.display = "none";
    }
  }
}

// Sign in
function Signin() {}
