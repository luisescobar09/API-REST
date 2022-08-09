function validateSession(){
    token = sessionStorage.getItem('token')
    if (token != null) {
            window.location.replace("home/")
    }
}

function login() {
    var re = /\S+@\S+\.\S+/;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    if (email.length == 0 || password.length == 0) {
            alert("Faltan datos por llenar");
    }
    else {
            if (re.test(email) === true) {
                    if (password.length < 6) {
                            alert("La contraseña debe ser mayor a 6 caracteres.")
                            document.getElementById("password").focus();
                    }
                    else {
                            sendRequest(email, password);
                    }        
            }
            else {
                   alert("Verifique la dirección de correo ingresada.")
                   document.getElementById("email").focus(); 
            }
    }
}
function sendRequest(email, password) {
    var request = new XMLHttpRequest();
    request.open("GET", "http://localhost:8000/users/validate/", true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Basic " + btoa(email+ ":" + password))
    request.setRequestHeader("Content-Type", "application/json");
     
    request.onload = () => {
            const response = request.responseText;
            const json = JSON.parse(response);
            //console.log("JSON:", json);

            if (request.status === 202) {
                    sessionStorage.setItem("token", json.token)
                    window.location.replace("home/");
            }
            else if (request.status === 401) {
                    alert(json.detail);
                    if (json.detail.search("correo") != -1) {
                            document.getElementById("email").focus();
                    }
                    else {
                            document.getElementById("password").focus();
                    }
            }
            else {
                    alert(json.detail);
                    window.location.replace("/");
            }
    }
    request.send();
}