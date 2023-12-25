
function getCookie(name){
    let cookieValue = null;
    if (document.cookie && document.cookie !== ""){
        const cookies = document.cookie.split(";");
        for(let i=0;i<cookies.length; i++){
            const cookie = cookies[i].trim();
            if(cookie.substring(0, name.length + 1) === (name + "=")){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
  return cookieValue;
}
$(document).ready(function () {
    function updateCartTotalQuantity() {
        $.ajax({
            type: "GET",
            url: '/cartTotalQuantity/',
            dataType: "json",
            success: function (data) {
                var totalQuantity = data.cart_quantity;
                $('#total-count').text(totalQuantity);
            }
        });
    }

    // Call the function on page load to initialize the total count
    updateCartTotalQuantity();
});


// $('.plusCart').click(function () {
//     var id = $(this).children().attr("pid");
//     var eml = this.parentNode.children[2];
//     console.log(`plusCart${id}`);
//     $.ajax({
//         type: "POST",
//         url: '/plusCart/',
//         dataType: "json",
//         data: {
//             product_id: id,
//         },
//         headers: {
//             "X-Requested-with": "XMLHttpRequest",
//             "X-CSRFToken": getCookie("csrftoken"),
//         },
//         success: function (data) {
//             eml.innerText = data.quantity;
//             document.getElementById("amount").innerText = data.amount;
//             document.getElementById("totalamount").innerText = data.totalamount;
//         }
//     });
// });

// $('.minusCart').click(function () {
//     var id = $(this).children().attr("pid");
//     var eml = this.parentNode.children[2];
//     console.log(id);
//     $.ajax({
//         type: "POST",
//         url: '/minusCart/',
//         dataType: "json",
//         data: {
//             product_id: id,
//         },
//         headers: {
//             "X-Requested-with": "XMLHttpRequest",
//             "X-CSRFToken": getCookie("csrftoken"),
//         },
//         success: function (data) {
//             eml.innerText = data.quantity;
//             document.getElementById("amount").innerText = data.amount;
//             document.getElementById("totalamount").innerText = data.totalamount;
//         }
//     });
// });

// $('.RemoveCart').click(function () {
//     var id = $(this).attr("pid");
//     var eml = this;
//     console.log(id);
//     $.ajax({
//         type: "POST",
//         url: '/removeCart/',
//         dataType: "json",
//         data: {
//             product_id: id,
//         },
//         headers: {
//             "X-Requested-with": "XMLHttpRequest",
//             "X-CSRFToken": getCookie("csrftoken"),
//         },
//         success: function (data) {
//             console.log("delete");
//             document.getElementById("amount").innerText = data.amount;
//             document.getElementById("totalamount").innerText = data.totalamount;
//             eml.parentNode.parentNode.parentNode.parentNode.remove();
//         }
//     });
// });




