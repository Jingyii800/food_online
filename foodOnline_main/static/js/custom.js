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