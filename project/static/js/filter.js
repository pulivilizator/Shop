function togglePriceInput(el, id=null) {
  if (el === 'price') {
    let priceInput = document.getElementById("price_input");
    priceInput.classList.toggle("active"); 
  } 
  else if (el === 'checkbox') {
    let priceInput = document.getElementById(`${id}`);
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
function addParameter() {
    let searchInput = document.getElementById('search_input');
    let search_val = searchInput.value;
    if (search_val) {
      let form = document.getElementById("products__filter");
      let input = document.createElement("input");
      input.type = "hidden";
      input.name = "search";
      input.value = search_val;
      form.appendChild(input);
      form.submit();}
}