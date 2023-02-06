const themeSelector = document.getElementById("theme-selector");

themeSelector.addEventListener("change", function () {
  const currentTheme = document.getElementById("current-theme");
  if (currentTheme) {
    currentTheme.remove();
  }

  const selectedValue = themeSelector.value;
  const link = document.createElement("link");
  link.id = "current-theme";
  link.rel = "stylesheet";
  link.href = `$/static/css/{selectedValue}.css`;
  document.head.appendChild(link);
});