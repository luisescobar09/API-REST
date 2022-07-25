function validateSession(){
    token = sessionStorage.getItem('token')
    if (token != null) {
            window.location.replace("/home/")
    }
}

function signup() {
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
                            sendResquest(email, password);
                    }        
            }
            else {
                   alert("Verifique la dirección de correo ingresada.")
                   document.getElementById("email").focus(); 
            }
    }
}

function sendResquest(email, password) {
    var payload = {
            "email" : email,
            "password" : password
    }
    var request = new XMLHttpRequest();
    request.open("POST", "http://localhost:8000/user/", true);
    request.setRequestHeader("Content-Type", "application/json");
    //sessionStorage.setItem("tokenID", password)   
    request.onload = () => {
            const response = request.responseText;
            const json = JSON.parse(response);
            //console.log("JSON:", json);

            if (request.status === 201) {
                    alert(json.response);
                    window.location.replace("/");
            }
            else if (request.status === 409) {
                    alert(json.detail);
                    document.getElementById("email").focus();
            }
            else {
                    alert(json.detail);
                    window.location.replace("/");
            }
    }
    request.send(JSON.stringify(payload));
}