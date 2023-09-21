function togglePriceInput(el, id=null) {
  if (el === 'price') {
    var priceInput = document.getElementById("price_input");
    priceInput.classList.toggle("active"); 
  } 
  else if (el === 'checkbox') {
    var priceInput = document.getElementById(`${id}`);
    priceInput.classList.toggle("active"); 
  }
}

function resetFilters() {
  document.getElementById("min_price").value = "0";
  document.getElementById("max_price").value = "999999";
  var checkboxes = document.querySelectorAll("input[type='checkbox']");
  checkboxes.forEach(function(checkbox) {
    checkbox.checked = false;
  });
}
