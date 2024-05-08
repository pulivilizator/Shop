$(document).ready(function() {
    $(document).on('click', '.add_to_likes', function(event) {
        event.preventDefault();

        var productId = $(this).data('product-id');
        var button = $(this);

        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: '/add_to_likes/' + productId + '/',
            method: 'POST',
            dataType: 'json',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response.success) {
                    button.replaceWith('<div class="in_likes detail__product_like" data-product-id="' + productId + '"><i class="fa-solid fa-heart fa-lg" style="color: #f50505;"></i> В избранном</div>');
                }
                else {
                    alert(response.error);
                }
            }
        });
    });

    $(document).on('click', '.in_likes', function(event) {
        event.preventDefault();

        var productId = $(this).data('product-id');
        var button = $(this);

        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: '/remove_from_likes/' + productId + '/',
            method: 'POST',
            dataType: 'json',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response.success) {
                    button.replaceWith('<div class="add_to_likes detail__product_like" data-product-id="' + productId + '"><i class="fa-regular fa-heart fa-lg"></i> В избранное</div>');
                }
                else {
                    alert(response.error);
                }
            }
        });
    });

    $('.remove_button_likes').click(function() {
            var productId = $(this).data('product-id');

            $.ajax({
                url: '/remove_from_likes/' + productId + '/',
                type: 'GET',
                success: function(response) {
                    $(`#elem${productId}`).remove()
                }
            });
        });

    $('.clear_likes').click(function() {

        $.ajax({
            url: '/clear_likes/',
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