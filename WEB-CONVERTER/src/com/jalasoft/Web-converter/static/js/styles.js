const navStyles1 = document.getElementById("navStyles1");
const navStyles2 = document.getElementById("navStyles2");
const navStyles3 = document.getElementById("navStyles3");

navStyles1.addEventListener("click", function () {
  switchTheme("/static/css/base3.css");
});

navStyles2.addEventListener("click", function () {
  switchTheme("/static/css/base4.css");
});

navStyles3.addEventListener("click", function () {
  switchTheme("/static/css/base2.css");
});

function switchTheme(theme) {
  const currentTheme = document.getElementById("current-theme");
  if (currentTheme) {
    currentTheme.remove();
  }

  const link = document.createElement("link");
  link.id = "current-theme";
  link.rel = "stylesheet";
  link.href = theme;
  document.head.appendChild(link);

  localStorage.setItem("selected-theme", theme);
}
const selectedTheme = localStorage.getItem("selected-theme");
if (selectedTheme) {
  switchTheme(selectedTheme);
}