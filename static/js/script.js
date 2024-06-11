function initAutocomplete() {
  var input = document.getElementById("autocomplete");
  var autocomplete = new google.maps.places.Autocomplete(input);
  autocomplete.setFields(["address_components", "geometry", "icon", "name"]);
}
