$(document).ready(function() {
    $('#couponBTN').on('click', function (event) {
        event.preventDefault();

        var couponCode = $('#coupon').val();
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: '/apply/' + couponCode + '/',
            method: 'POST',
            dataType: 'json',
            headers: {'X-CSRFToken': csrftoken},
            success: function (response) {
                document.getElementById('couponNotExists').style.display='none'
                $('#cart__total_price').text('Итоговая сумма: ' + response.cart_total_price + ' руб.');
                $('#cart__discount').text('Ваша скидка: ' + response.cart_discount + ' руб.');
            },
            error: function(response) {
                document.getElementById('couponNotExists').style.display='block'
            }
        });
    });
});