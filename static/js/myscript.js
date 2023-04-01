

// $('.plus-cart').click(function(){
//     var id = $(this).attr("pid").toString();
//     var eml = this.parentNode.children[1]
//     console.log("pid =",id)
//     $.ajax({
//         type:"GET",
//         url:"pluscart/",
//         data:{
//             prod_id:id
//         },
//         success:function(data){
//             console.log("data = ",data);
//             eml.innerText=data.quantity
//             document.getElementById("price").innerText.price
//         }
//     })
// })
// $(document).ready(function () {
//     $(".plus-btn, .minus-btn").click(function (event) {
//         event.preventDefault();

//         var form = $(this).closest(".update-cart-form");
//         var product_id = form.find("input[name='product_id']").val();
//         var quantity = form.find("input[name='quantity']").val();
//         var url = form.attr("action");

//         $.ajax({
//             url: url,
//             method: "POST",
//             data: {
//                 product_id: product_id,
//                 quantity: quantity,
//                 csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
//             },
//             success: function (data) {
//                 location.reload();
//             },
//             error: function (errorData) {
//                 console.log("error");
//             },
//         });
//     });
// });