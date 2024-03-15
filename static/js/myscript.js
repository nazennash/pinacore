$(document).ready(function () {
    function updateCartCount() {
        $.ajax({
            url: '/get_cart_count/',
            success: function (response) {
                $('#cart-count').text(response.cart_count);
            },
            error: function (xhr, errmsg, err) {
                console.log('Error fetching cart count:', errmsg);
            },
        });
    }

    function updateCart() {
        $.ajax({
            url: '/showCart/',
            success: function (response) {
                $('#cart-count').text(response.cart_count);
                $('#cart-content').html(response.html);
            },
            error: function (xhr, errmsg, err) {
                console.log('Error updating cart:', errmsg);
            },
        });
    }

    function addToCart(prod_id) {
        $.ajax({
            type: 'GET',
            url: '/plus_cart/',
            data: { prod_id: prod_id },
            success: function () {
                updateCart();
            },
            error: function (xhr, errmsg, err) {
                console.log('Error adding item to cart:', errmsg);
            },
        });
    }

    function removeFromCart(prod_id) {
        $.ajax({
            type: 'GET',
            url: '/minus_cart/',
            data: { prod_id: prod_id },
            success: function () {
                updateCart();
            },
            error: function (xhr, errmsg, err) {
                console.log('Error removing item from cart:', errmsg);
            },
        });
    }

    function removeItemFromCart(prod_id) {
        $.ajax({
            type: 'GET',
            url: '/remove_cart/',
            data: { prod_id: prod_id },
            success: function () {
                updateCart();
            },
            error: function (xhr, errmsg, err) {
                console.log('Error removing item from cart:', errmsg);
            },
        });
    }

    $('.plus-cart').click(function (e) {
        e.preventDefault();
        var prod_id = $(this).attr('pid');
        addToCart(prod_id);
    });

    $('.minus-cart').click(function (e) {
        e.preventDefault();
        var prod_id = $(this).attr('pid');
        removeFromCart(prod_id);
    });

    $('.remove-cart').click(function (e) {
        e.preventDefault();
        var prod_id = $(this).attr('pid');
        removeItemFromCart(prod_id);
    });

    $.ajaxSetup({ cache: false });

    updateCartCount();
});
