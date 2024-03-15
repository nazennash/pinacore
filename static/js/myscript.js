$(document).ready(function () {
    function updateCartCount() {
        $.ajax({
            url: '/get_cart_count/',
            success: function (response) {
                $('#cart-count').text(response.cart_count);
            },
            error: function (xhr, errmsg, err) {
                console.log('Error fetching cart count');
            },
        });
    }

    updateCartCount();

    function updateCart() {
        $.ajax({
            url: '/showCart/',
            success: function (response) {
                $('#cart-count').text(response.cart_count);

                $('#cart-content').html(response.html);
            },
            error: function (xhr, errmsg, err) {
                console.log('Error updating cart');
            },
        });
    }

    $('.plus-cart').click(function (e) {
        e.preventDefault();
        var prod_id = $(this).attr('pid');

        $.ajax({
            type: 'GET',
            url: '/plus_cart/',
            data: { prod_id: prod_id },
            success: function (response) {
                updateCart();
            },
            error: function (xhr, errmsg, err) {
                console.log('Error adding item to cart');
            },
        });
    });

    $('.minus-cart').click(function (e) {
        e.preventDefault();
        var prod_id = $(this).attr('pid');

        $.ajax({
            type: 'GET',
            url: '/minus_cart/',
            data: { prod_id: prod_id },
            success: function (response) {
                updateCart();
            },
            error: function (xhr, errmsg, err) {
                console.log('Error removing item from cart');
            },
        });
    });

    $('.remove-cart').click(function (e) {
        e.preventDefault();
        var prod_id = $(this).attr('pid');

        $.ajax({
            type: 'GET',
            url: '/remove_cart/',
            data: { prod_id: prod_id },
            success: function (response) {
                updateCart();
            },
            error: function (xhr, errmsg, err) {
                console.log('Error removing item from cart');
            },
        });
    });

    updateCartCount();
});
