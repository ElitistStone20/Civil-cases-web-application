var btnLogin = document.getElementById("login");
var btnRegister = document.getElementById("register");
var button = document.getElementById("btn");   
     
// Animations for the login and register options
// MOves the colour to the selected button
function register(){
    btnLogin.style.left = "-400px";
    btnRegister.style.left = "50px";
    button.style.left = "110px";
}
function login(){
    btnLogin.style.left = "50px";
    btnRegister.style.left = "450px";
    button.style.left = "0";
}

// Verifies the two passwords entered
function validate(){
    console.log("Clicked");
    var id = document.getElementById("identification").value;
    var password_main = document.getElementById("password-main").value;
    var password_verify = document.getElementById("password-verify").value;
    var type = document.getElementById("combobox").value;
    console.log(id);
    if (isNaN(id) && type == "Barrister" || type == "Solicitor") {
        document.getElementById("error-message").innerHTML = "Identification number must be a number";       
        return false;
    }
    if (password_main != password_verify) {
        document.getElementById("error-message").innerHTML = "Passwords do not match";        
        return false;
    }
    return true;
}

// Function that checks if the type input has been changed and 
// if the value is not present in the selction options changes it
function check_type_change(){
    var type_text_box = document.getElementById("combobox");
    var selection_box = document.getElementById("selection_box");
    if (type_text_box.value == selection_box.value) {
        return true;
    }
    type_text_box.value = selection_box.options[selection_box.selectedIndex].innerHTML;
    return false;
}

// Copies the value selected in the selection box to the textbox
function combo(thelist, theinput){
    theinput = document.getElementById(theinput);
    var idx = thelist.selectedIndex;
    var content = thelist.options[idx].innerHTML;
    theinput.value = content;
}