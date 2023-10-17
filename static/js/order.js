document.addEventListener("DOMContentLoaded", function() {
  var totalValueElement = document.querySelector(".total__value");
  var deliveryValueElement = document.querySelector(".delivery.ordifm .value");
  var initialTotalValue = parseFloat(totalValueElement.textContent.replace(" руб.", ""));

  var deliveryMethodRadios = document.getElementsByName("delivery_method");
  for (var i = 0; i < deliveryMethodRadios.length; i++) {
    deliveryMethodRadios[i].addEventListener("change", function() {
      var selectedPrice = this.parentNode.querySelector(".label__price").textContent;

      var price;
      if (selectedPrice === "Бесплатно" || selectedPrice === "бесплатно") {
        price = 0;
      } else {
        price = parseFloat(selectedPrice.replace(" руб.", ""));
      }

      totalValueElement.textContent = (initialTotalValue + price) + " руб.";

      deliveryValueElement.textContent = price + " руб.";
    });
  }
});