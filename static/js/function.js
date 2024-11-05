$(".add-to-cart").on("click", function(){
    let this_val = $(this)
    let index = this_val.attr("data-index")
    let quantity = $(".product-quantity-" + index).val()
    let product_name = $(".product-name-" + index).val()
    let product_price = $(".product-price-" + index).text()
    let product_id = $(".product-id-" + index).val()
    let product_image = $(".product-image-" + index).val()

    console.log("Quantity:", quantity);
    console.log("product_name:", product_name);
    console.log("product_price:", product_price);
    console.log("product_id:", product_id);
    console.log("this_val:", this_val);
    console.log("product-image:", product_image);

    $.ajax({
      url: '/add-to-cart',
      data: {
          'id': product_id,
          'qty': quantity,
          'title': product_name,
          'price': product_price,
          'image': product_image,
      },
      dataType: 'json',
      beforeSend: function(){
          console.log("Adding Product to Cart....");
      },
      success: function(response){
          this_val.html("Item Added To Cart")
          console.log("Added Product to Cart!");
          $(".cart-item-count").text(response.totalcartitems)
      }

    })

})

$(".delete-item").on("click", function(){
    let this_val = $(this)
    let product_id = this_val.attr("data-product")


    console.log("product_id:", product_id);

    $.ajax({
      url: '/delete_from_cart',
      data: {
          'id': product_id,

      },
      dataType: 'json',
      beforeSend: function(){
          this_val.hide()
          console.log("Deleting Product from Cart....");
      },
      success: function(response){
          this_val.show()
          $("#cart-list").html(response.data)
          console.log("Item deleted from Cart");
          $(".cart-item-count").text(response.totalcartitems)
      }

    })

})


$(document).ready(function(){
    $(".filter-checkbox").on("click", function(){
        console.log("checkbox has been clicked....");
        let filter_object = {}

        $(".filter-checkbox").each(function(){
              let filter_value = $(this).val()
              let filter_key = $(this).data("filter")

              filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter='+ filter_key +']:checked')).map(function(element){
                    return element.value
              })
        })
        console.log("filter object is:", filter_object);
        $.ajax({
          url: '/filter-products',
          data: filter_object,
          dataType: 'json',
          beforeSend: function(){
            console.log("sending data....");
          },
          success: function(response){
            console.log("data sent....");
            console.log(response);
            $("#filter_product").html(response.data)
           }
        })
    })
})

$(".email-form").submit(function(e){
    e.preventDefault();
    console.log("button clicked.....");

      $.ajax({
          data: $(this).serialize(),
          method: $(this).attr("method"),
          url: $(this).attr("action"),
          dataType: 'json',

          success: function(res){
            console.log("comment save to DB....");
           $(".subscribe-success").html("Hello you have successfully sign up ..")
           $(".email-form").hide()

          }
     })
 })

const monthNames = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June',
  'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'
];
$("#comment-form").submit(function(e){
    e.preventDefault();
    console.log("button clicked.....");

    let dt = new Date();
    let time = dt.getDay() + "" + monthNames[dt.getUTCMonth()] + "," + dt.getFullYear()

    $.ajax({
          data: $(this).serialize(),
          method: $(this).attr("method"),
          url: $(this).attr("action"),
          dataType: 'json',

          success: function(res){
            console.log("comment save to DB....");

           if(res.bool == true){
           $(".review-res").html("Review added successfully..")
           $("#comment-form").hide()

           let _html = '<div class="col-md-6">'

               _html += '<h4 class="mb-4">'+ res.context.review.count + 'review for' + res.context.product.name + '</h4>'
               _html += '<div class="media mb-4">'
               _html += '<img src="img/user.jpg" alt="Image" class="img-fluid mr-3 mt-1" style="width: 45px;">'
               _html += '<div class="media-body">'
               _html += '<h6>'+ res.context.user +'<small> - <i>'+ time +'</i></small></h6>'
               _html += '<div class="text-primary mb-2">'
               _html += '<i class="fas fa-star"></i>'
               _html += '<i class="fas fa-star"></i>'
               _html += '<i class="fas fa-star"></i>'
               _html += '<i class="fas fa-star-half-alt"></i>'
               _html += '<i class="fas fa-star"></i>'
               _html += '</div>'
               _html += '<p>'+ res.context.review +'</p>'
               _html += '</div>'
               _html += '</div>'
               _html += '</div>'
               $(".comment-list").prepend(_html)
           }
           }
        })
    })

$(".address-form").submit(function(e){
    e.preventDefault();
    console.log("button clicked.....");

      $.ajax({
          data: $(this).serialize(),
          method: $(this).attr("method"),
          url: $(this).attr("action"),
          dataType: 'json',

          success: function(res){
            console.log("address save to DB....");
           $(".address-success").html("Hello you have successfully submitted your shipping address ..")
           $(".address-form").hide()

          }
     })
 })

 $("#contactForm").submit(function(e){
    e.preventDefault();
    console.log("button clicked.....");

      $.ajax({
          data: $(this).serialize(),
          method: $(this).attr("method"),
          url: $(this).attr("action"),
          dataType: 'json',

          success: function(res){
            console.log("message save to DB....");
           $(".contact-success").html("Hello your message has been received..")
           $("#contactForm").hide()

          }
     })
 })