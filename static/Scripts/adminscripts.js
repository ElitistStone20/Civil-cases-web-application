var barrister_array = [];
var solicitor_array = [];
var courts_array = [];
var address_array = [];


// Edit a row. Get the index of the row where the button instance was clicked
$(function() {
    $('button.edit-button').on('click', function(){
        var tablename = $(this).closest('table').attr('id');
        var row = $(this).parents("tr");
        var array = $('td', row).map(function(index, td) {
            return $(td).text();
        })
        switch (tablename){
            case "solicitors":
                Solicitor_Edit(array);
                break;
            case "barristers":
                Barrister_Edit(array);
                break;
            case "courts":
                Court_Edit(array);
                break;
            case "addresses":
                Address_Edit(array);
                break;
            case "cases":
                Case_Edit(array);
                break;
            case "clients":
                Client_Edit(array);
                break;
            default:
                console.log("Table not found");
        }
    })
})

window.onload = function() {
    $("table#barristers").each(function(){
        console.log("loading");
        var row = []
        var tableData =  $(this).find('td');
        if (tableData.length > 0){
            tableData.each(function(){
                row.push($(this).text());
            })
            barrister_array.push(row);
        }
    });
    
    $("table#barristers").each(function(){
        console.log("loading");
        var row = []
        var tableData =  $(this).find('td');
        if (tableData.length > 0){
            tableData.each(function(){
                row.push($(this).text());
            })
            barrister_array.push(row);
        }
    });

}

//Delete row
$(function() {
    $('button.delete-button').on('click', function(){
        var index = $(this).closest('tr').index();
        $(this).closest('tr').remove();       
    })
})

function combo(thelist, theinput){
    theinput = document.getElementById(theinput);
    var idx = thelist.selectedIndex;
    var content = thelist.options[idx].innerHTML;
    theinput.value = content;
}

function Barrister_Edit(row){
    var bar_council = document.getElementById("bar-council");
    var title = document.getElementById("title-barrister");
    var firstname = document.getElementById("first-name-barrister");
    var middlename = document.getElementById("middle-name-barrister");
    var surname = document.getElementById("surname-barrister");
    var password = document.getElementById("password-barrister");
    var phone_number = document.getElementById("phonenumber-barrister");
    var address_combo = document.getElementById("address-combo");

    bar_council.value = row[0];
    title.value = row[1];
    firstname.value = row[2];
    middlename.value = row[3];
    surname.value = row[4];
    password.value = row[5];
    phone_number.value = row[6];

    console.log(row[7].trim());
    
    for (idx = 0; idx < address_combo.length; idx++){      
        if (address_combo.options[idx].value.includes(row[7].trim())){
            address_combo.selectedIndex = idx;
            console.log("Contains address");
            return;
        }
    }
}

function Solicitor_Edit(row) {
    var reference = document.getElementById("reference-id");
    var title = document.getElementById("title-solicitor");
    var firstname = document.getElementById("firstname-solicitor");
    var middlename = document.getElementById("middle-name-solicitor");
    var surname = document.getElementById("surname-solicitor");
    var password = document.getElementById("password-solicitor");
    var type = document.getElementById("combo-box");

    reference.value = row[0];
    title.value = row[1];
    firstname.value = row[2];
    middlename.value = row[3];
    surname.value = row[4];
    password.value = row[5];
    type.value = row[6];
}

function Court_Edit(row) {
    var court_id = document.getElementById("court-id");
    var name = document.getElementById("court-name");
    var username = document.getElementById("court-user-name");
    var password = document.getElementById("court-password");
    var type = document.getElementById("combo-box");

    court_id.value = row[0];
    name.value = row[1];
    username.value = row[2];
    password.value = row[3];
    type.value = row[4];
}

function Address_Edit(row) {
    var address_id = document.getElementById("address-id");
    var house_number = document.getElementById("house-number");
    var street_name = document.getElementById("street-name");
    var town_name = document.getElementById("town-name");
    var city = document.getElementById("city");
    var country = document.getElementById("country");
    var postcode = document.getElementById("postcode");

    address_id.value = row[0];
    house_number.value = row[1];
    street_name.value = row[2];
    town_name.value = row[3];
    city.value = row[4];
    country.value = row[5];
    postcode.value = row[6];
}

function Case_Edit(row){
    var claim_id = document.getElementById("claim-id");
    var title = document.getElementById("case-title");
    var status = document.getElementById("status");
    var start_date = document.getElementById("start-date");
    var end_date = document.getElementById("end-date");
    var description = document.getElementById("description");
    var result = document.getElementById("result-of-case");
    var type = document.getElementById("type");

    claim_id.value = row[0];
    title.value = row[1];
    status.value = row[2];
    start_date.value = row[3];
    end_date.value = row[4];
    description.value = row[5];
    result.value = row[6];
    type.value = row[7];
}

function Client_Edit(row){
    var id = document.getElementById("client-id");
    var title = document.getElementById("client-title");
    var firstname = document.getElementById("client-firstname");
    var middlename= document.getElementById("client-middlename");
    var surname = document.getElementById("client-surname");
    var dob = document.getElementById("client-dob");
    var phone_number = document.getElementById("client-phonenumber");
    var address_combo = document.getElementById("client-address");

    id.value = row[0];
    title.value = row[1];
    firstname.value = row[2];
    middlename.value = row[3];
    surname.value = row[4];
    dob.value = row[5];
    phone_number.value = row[6];

    if (address_combo == null){
        console.log("Address is null");
    }

    console.log(row[7].trim());

    for (idx = 0; idx < address_combo.length; idx++){
        console.log(address_combo.options[idx].value);
        if (address_combo.options[idx].value.includes(row[7].trim())){
            address_combo.selectedIndex = idx;
            console.log("Contains client address");
            return;
        }
    }
}

function validate_address_submission(){
    var house_number = document.getElementById("house-number").value;
    var postcode = document.getElementById("postcode").value;
    postcode = postcode.replace(/\s/g, "");
    var regex = /^[A-Z]{1,2}[0-9]{1,2} ?[0-9][A-Z]{2}$/i;
    if (isNaN(house_number)){
        alert("House number must be a number!");
        return false;
    }
    else if (postcode.length > 8 || !regex.test(postcode)){
        alert("Postcode is not formatted correctly!");
        return false;
    }
    return true;
}

function validate_case_submission() {
    var claim_id = document.getElementById("claim-id").value;
    if (isNaN(claim_id)){
        alert("Claim ID must be a number!");
        return false;
    }
    return true;
}

function validate_solicitor_submission(){
    var reference_id = document.getElementById("reference-id").value;
    if (isNaN(reference_id)){
        alert("Reference ID must be a number!");
        return false;
    }
    return true;
}

function validate_barrister_submission(){
    var bar_council = document.getElementById("bar-council").value;
    var phone_number = document.getElementById("phonenumber-barrister").value;
    var number_template = /^\+?([0-9]{2})\)?[-. ]?([0-9]{4})[-. ]?([0-9]{4})$/;
    if (isNaN(bar_council) || !phone_number.match(number_template)) {
        alert("Phone number is not formatted correctly!");
        return false;
    }
    return true;
}