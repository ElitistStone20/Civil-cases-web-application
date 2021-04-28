function validate_search_assign(){
    var search_item = document.getElementById("search-assigned").value.trim().toString();
    if (isNaN(search_item)){
        alert("Claim ID must be a number!");
        return false;
    }
    return true;
}

function validate_search_all(){
    var search_item = document.getElementById("search-cases").value.trim().toString();
    if (isNaN(search_item)){
        alert("Claim ID must be a number!");
        return false;
    }
    return true;
}