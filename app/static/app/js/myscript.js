$(document).ready(function() {
    $('#slider1, #slider2, #slider3, #slider4').owlCarousel({
        loop: true,
        margin: 20,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                nav: false,
                autoplay: true
            },
            600: {
                items: 3,
                nav: true,
                autoplay: true
            },
            1000: {
                items: 5,
                nav: true,
                loop: true,
                autoplay: true
            }
        }
    });
});


$('.plus-cart').click(function() {
    var id = $(this).attr('pid');
    var ele = this.parentNode.children[2]
    $.ajax({
        type: 'GET',
        url: '/pluscart',
        data:{
            prod_id: id
        },
        success: function(data) {
            ele.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.tamount
        }
    })
});


$('.minus-cart').click(function() {
    var id = $(this).attr('pid');
    var ele = this.parentNode.children[2]
    $.ajax({
        type: 'GET',
        url: '/minuscart',
        data:{
            prod_id: id
        },
        success: function(data) {
            ele.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.tamount
        }
    })
});

$('.remove-cart').click(function() {
    var id = $(this).attr('pid');
    var ele = this
    $.ajax({
        type: 'GET',
        url: '/removecart',
        data:{
            prod_id: id
        },
        success: function(data) {
            ele.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.tamount
            ele.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
});