<script>
  var select = document.getElementById("styleSelect");
  select.addEventListener("change", function() {
    var selectedValue = select.value;
    if (selectedValue) {
      var link = document.getElementById("stylesheet");
      link.setAttribute("href", selectedValue);
    }
  });
</script>