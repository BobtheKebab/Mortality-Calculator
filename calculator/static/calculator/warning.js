function choice1(select) {
    if(select.options[select.selectedIndex].text == "Sex" || select.options[select.selectedIndex].text == "Ethnicity") {
        alert("Please select a valid option");
    }
}

function validateForm(){
    var sex = document.getElementById("Sex");
    var ethnicity = document.getElementById("Ethnicity");

    if (!(sex.value == "Please select" || ethnicity.value == "Please select")){
        return true;
    }
    else{
        alert("Please fill in the drop downs");
        return false;
    }
}

function fillDropdowns(causes) {
    var cause1 = document.getElementById("cause1");
    var cause2 = document.getElementById("cause2");

    for (const cause of causes) {
        var option = document.createElement("option");
        option.value = cause;
        option.text = cause;
        cause1.appendChild(option);
        cause2.appendChild(option);
    }
}