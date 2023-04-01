// $(document).ready(function () {
//     $('.changeQuantity').click(function (e) {
//         e.preventDefault();
        
//         var product_id = $(this).closest('.cart_data').find('.prod_id').val();
//         var varient_id = $(this).closest('.cart_data').find('.varient_id').val();
//         var product_qty =  $(this).closest('.cart_data').find('.quantity-input').val();
//         var token = $('input[name=csrfmiddlewaretoken]').val();
//         $.ajax({
//             method: "POST",
//             url: "/shop/addcartitem",
//             data: {
//                 'product_id':product_id,
//                 'varient_id':varient_id,
//                 'product_qty':product_qty,
//                 csrfmiddlewaretoken:token

//             },
//             success: function (response) {
//                 alertify.success(response.status)
//             }
//         });
//     });
// });

$(document).ready(function () {
    $('.changeQuantity').click(function (e) {
        e.preventDefault();
        
        var product_id = $(this).closest('.cart_data').find('.prod_id').val();
        console.log(product_id)
        var varient_id = $(this).closest('.cart_data').find('.varient_id').val();
        console.log(varient_id)
        var product_qty =  $(this).closest('.cart_data').find('.quantity-input').val();
        console.log(product_qty)
        var token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            method: "POST",
            url: "{% url 'addcartitem' %}",
            data: {
                'product_id':product_id,
                'varient_id':varient_id,
                'product_qty':product_qty,
                csrfmiddlewaretoken:token

            },
            success: function (response) {
                if (response.status === "Updated Successfully") {
                    var new_quantity = response.new_quantity;
                    $(this).closest('.cart_data').find('.quantity-input').val(new_quantity);
                    alertify.success(response.status);
                } else {
                    alertify.error(response.status);
                }
            }
        });
    });

// add to cart
    $("#addToCart").on('click', function (){
        var qty=$("#product_qty").val();
        var product_id=$(".product_id").val();
        var varient_id=$(".varient_id").val();
        console.log(qty,product_id,varient_id)
       

    });


});
