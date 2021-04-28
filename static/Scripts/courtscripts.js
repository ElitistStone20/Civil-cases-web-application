$(function() {
    $('button.edit-button').on('click', function(){
        var tablename = $(this).closest('table').attr('id');
        var row = $(this).parents("tr");
        var array = $('td', row).map(function(index, td){
            return $(td).text();
        })
        Case_Edit(array);
    })
})

function Case_Edit(row){
    var claim_num = document.getElementById("claim-id");
    var case_title = document.getElementById("case-title");
    var status = document.getElementById("case-status");
    var start_date = document.getElementById("case-start-date");
    var end_date = document.getElementById("case-end-date");
    var description = document.getElementById("case-description");
    var result = document.getElementById("case-result");
    var type = document.getElementById("case-type");
    var solicitor = document.getElementById("case-solicitor");
    var client = document.getElementById("case-client");

    claim_num.value = row[0];
    case_title.value = row[1];
    start_date.value = row[3];
    end_date.value = row[4];
    description.value = row[5];
    result.value = row[6];
    type.value = row[7];    
    
    populate_combo(solicitor, row[8].trim());
    populate_combo(client, row[9].trim());
    populate_combo(status, row[2].trim())

    function populate_combo(combo, search_val){
        for (idx = 0; idx < combo.length; idx++){
            if (combo.options[idx].value.includes(search_val)){
                combo.selectedIndex = idx;
            }
        }
    } 
}

function validate_case_submission(){
    var start_date = document.getElementById("case-start-date").value;
    var end_date = document.getElementById("case-end-date").value;
    
    if (start_date != null || start_date != "" && test_date(start_date) == false){
        return false;
    }
    if (end_date != null || end_date != "" && test_date(end_date) == false){
        return false;
    }


    function test_date(date){
        var date_pattern = new RegExp("^([0-9]{2,4})-([0-1][0-9])-([0-3][0-9])(?:( [0-2][0-9]):([0-5][0-9]):([0-5][0-9]))?(.[0-9]{1,6})?$");
        if (date_pattern.test(date)){
            return true;
        } else {
            return false;
        }
    }
    
}