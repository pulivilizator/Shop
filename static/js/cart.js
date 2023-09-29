$(document).ready(function() {
    $(document).on('click', '.add_to_cart', function(event) {
        event.preventDefault();

        var productId = $(this).data('product-id');
        var button = $(this);

        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: '/add_to_cart/' + productId + '/',
            method: 'POST',
            dataType: 'json',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response.success) {
                    if (button[0].classList.contains('buy__addcart')) {
                        button.replaceWith('<button class="in-cart buy__addcart" data-product-id="' + productId + '"><i class="fa-solid fa-check fa-2xl"></i> Товар в корзине</button>');
                    }
                    else if (button[0].classList.contains('basket__button')) {
                        button.replaceWith('<button class="in-cart basket__button" data-product-id="' + productId + '"><i class="fa-solid fa-check fa-2xl"></i></button>');
                    }
                }
                else {
                    alert(response.error);
                }
            }
        });
    });

    $(document).on('click', '.in-cart', function(event) {
        event.preventDefault();

        var productId = $(this).data('product-id');
        var button = $(this);

        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: '/remove_from_cart/' + productId + '/',
            method: 'POST',
            dataType: 'json',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response.success) {
                    if (button[0].classList.contains('buy__addcart')) {
                        button.replaceWith('<button class="add_to_cart buy__addcart" data-product-id="' + productId + '"><i class="fa-solid fa-basket-shopping fa-lg"> В корзину</button>');
                    } else if (button[0].classList.contains('basket__button')) {
                        button.replaceWith('<button class="add_to_cart basket__button" data-product-id="' + productId + '"><i class="fa-solid fa-basket-shopping fa-2xl"></button>');
                    }
                } else {
                    alert(response.error);
                }
            }
        });
    });

    $('.plus').click(function() {
        var productId = $(this).data('product-id');
        var quantity = $(this).data('quantity');

        $.ajax({
            url: '/add_to_cart/' + productId + '/',
            type: 'GET',
            success: function(response) {
                $(`#quantity${productId}`).text(`${response.new_quantity} руб.`);
                $(`#totalPrice${productId}`).text(`${response.total_price} руб.`);
                $('#cart__total_price').text(`Итоговая сумма: ${response.cart_total_price} руб.`);
            }
        });
    });

    $('.minus').click(function() {
        var productId = $(this).data('product-id');
        var quantity = $(this).data('quantity');

        $.ajax({
            url: '/delete_from_cart/' + productId + '/',
            type: 'GET',
            success: function(response) {
                $(`#quantity${productId}`).text(response.new_quantity);
                $(`#totalPrice${productId}`).text(response.total_price);
                $('#cart__total_price').text(`Итоговая сумма: ${response.cart_total_price} руб.`);
            }
        });
    });

    $('.remove_button').click(function() {
        var productId = $(this).data('product-id');

        $.ajax({
            url: '/remove_from_cart/' + productId + '/',
            type: 'GET',
            success: function(response) {
                $(`#elem${productId}`).remove()
                $('#cart__total_price').text(`Итоговая сумма: ${response.cart_total_price} руб.`);
            }
        });
    });

        $('.clear').click(function() {

        $.ajax({
            url: '/clear_cart/',
            type: 'GET',
            success: function(response) {
                 location.reload();
            }
        });
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}