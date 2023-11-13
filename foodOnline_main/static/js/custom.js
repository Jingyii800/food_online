let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['us']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }

    // get the address components and assign them to the fields
    var geocoder = new google.maps.Geocoder()
    // seperate the address from place
    var address = document.getElementById('id_address').value
    geocoder.geocode({'address':address}, function(results, status) {
        // console.log('results =>', results) // contains address
        // console.log('status=>', status)  // status: ok
        if (status == google.maps.GeocoderStatus.OK){ // get lat and longt
            var latitude = results[0].geometry.location.lat()
            var longtitude = results[0].geometry.location.lng()
            // Jquery to fill the field of form
            $(`#id_lattitude`).val(latitude)
            $(`#id_longtitude`).val(longtitude)

            $(`#id_address`).val(address)
        }
    })

    // loop through address component and assign other data
    for (var i = 0; i < place.address_components.length; i ++){
        for (var j = 0; j < place.address_components[i].types.length; j++){
            // get country
            if (place.address_components[i].types[j]=='country'){
                $(`#id_country`).val(place.address_components[i].long_name)
            }
            //get state
            if(place.address_components[i].types[j]=='administrative_area_level_1'){
                $(`#id_state`).val(place.address_components[i].long_name)
            }
            // get city
            if(place.address_components[i].types[j]=='locality'){
                $(`#id_state`).val(place.address_components[i].long_name)
            }
            // get zipcode
            if(place.address_components[i].types[j]=='postal_code'){
                $(`#id_zip_code`).val(place.address_components[i].long_name)
            }
        }
    }
}

// Ajax request
$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault()
        // retrieve food_id and url and data from dom
        food_id = $(this).attr('data-id')
        url = $(this).attr('data-url')
        $.ajax({
            type: 'GET',
            url: url, // already has the food-id in this url
            success: function(response){
                // display real-time cart count
                if (response.status == 'login_required'){
                    Swal.fire({
                        text: response.message,
                        icon: "info"
                      }).then(function(){
                        window.location = '/login' // click o to direct to login page
                      })
                }else if(response.status == 'Failed'){
                    Swal.fire({
                        text: response.message,
                        icon: "error"
                    })
                }
                else{
                    $('#cart-counter').html(response.cart_count['cart_count'])
                    $(`#qty-`+food_id).html(response.qty) //quantity for each

                    applyCartAmounts(response.cart_amount['subtotal'], 
                    response.cart_amount['tax'],response.cart_amount['total'])
                }
            }
        })
    })

    $('.decrease_cart').on('click', function(e){
        e.preventDefault()
        // retrieve food_id and data and url from dom
        food_id = $(this).attr('data-id')
        cart_id = $(this).attr('id')
        url = $(this).attr('data-url')
        $.ajax({
            type: 'GET',
            url: url, 
            // already has the food-id in this url 
            //from 'path('decrease_cart/<int:food_id>''
            // and "{% url 'decrease_cart' food.id %}"
            success: function(response){
                //display
                if (response.status == 'login_required'){
                    Swal.fire({
                        text: response.message,
                        icon: "info"
                      }).then(function(){
                        window.location = '/login' // click o to direct to login page
                      })
                }else if(response.status == 'Failed'){
                    Swal.fire({
                        text: response.message,
                        icon: "error"
                    })
                }
                else{
                    $('#cart-counter').html(response.cart_count['cart_count'])
                    $(`#qty-`+food_id).html(response.qty)
                    
                    if(window.location.pathname =='/marketplace/cart/'){
                        removeCartitem(response.qty, cart_id)
                        checkEmptyCart()
                    }

                    applyCartAmounts(response.cart_amount['subtotal'], 
                    response.cart_amount['tax'],response.cart_amount['total'])
                }
            }
        })
    })

    $('.delete_cart').on('click', function(e){
        e.preventDefault()
        cart_id = $(this).attr('data-id')
        url = $(this).attr('data-url')
        $.ajax({
            type:'GET',
            url: url,
            success: function(response){
                //display message
                if (response.status=='login_required'){
                    Swal.fire({
                        text: response.message,
                        icon: "info"
                    }).then(function(){
                        window.location = '/login'
                    })
                } else if(response.status=='Failed'){
                    Swal.fire({
                        text: response.message,
                        icon: "error"
                    })
                }else{
                    $('#cart-counter').html(response.cart_count['cart_count'])
                    Swal.fire({
                        text: response.message,
                        icon:'success'
                    })

                    removeCartitem(0, cart_id)
                    checkEmptyCart()

                    applyCartAmounts(response.cart_amount['subtotal'], 
                    response.cart_amount['tax'],response.cart_amount['total'])

                }
            }
        })
    })

    // delete the cart item if the qty is 0
    function removeCartitem(cartitemQty, cart_id){
        // only when user is in the cart page
            if (cartitemQty <= 0){
                // remove the item
                document.getElementById('cart-item-'+cart_id).remove()
            }
    }

    //check cart if empty display empty
    function checkEmptyCart(){
        var cart_count = document.getElementById('cart-counter').innerHTML
        if (cart_count== 0) {
            document.getElementById('empty-cart').style.display = "block"
        }
    }

    //apply cart amounts
    function applyCartAmounts(subtotal, tax, total){
        if(window.location.pathname == '/marketplace/cart/'){
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(total)
        }
    }

    // place each quantity for each food item
    // necessary!!!
    // initialize the page (retrieve from database)
    // if not having this, initial count will display 0
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $(`#`+the_id).html(qty)
    })
})