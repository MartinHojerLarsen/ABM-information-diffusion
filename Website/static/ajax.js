// AJAX test - succes

// getting the form
let ajaxform = document.getElementById("ajaxform");

// listening for submits
ajaxform.addEventListener("submit", function(e){
    // getting the two input values
    let a = parseInt(ajaxform.elements["numberA"].value);
    let b = parseInt(ajaxform.elements["numberB"].value);
    let htmlResult = document.getElementById("ajaxresult");   
    result = a + b;
    
    // showing result on website
    htmlResult.innerHTML = result;
    console.log(result);

    // preventing refresh
    e.preventDefault();

    // AJAX variable - parsing to server
    let server_data = [
        {"A": a},
        {"B": b}
    ];
        
    // AJAX handling - sending data as JSON 
    $.ajax({
        type: "POST", 
        url: "/ajax",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json',
    })
    
    
});
