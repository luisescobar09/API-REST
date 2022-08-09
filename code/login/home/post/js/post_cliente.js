function post_cliente() {
    var nombre = document.getElementById("nombre").value;
    var email = document.getElementById("email").value;
    var re = /\S+@\S+\.\S+/;
    if (email.length == 0 || nombre.length == 0) {
            alert("Faltan datos por llenar");
    }
    else {
            if (re.test(email) === true) {
                    console.log("ESTÁ AQUÍ")
                    token = sessionStorage.getItem('token')
                    if (token != null) {
                            var payload = {
                                    "nombre" : nombre,
                                    "email" : email
                            }
                            var request = new XMLHttpRequest();
                            request.open("POST", "http://localhost:8000/clientes/", true);
                            request.setRequestHeader("Accept", "application/json");
                            request.setRequestHeader("Authorization", "Bearer " + token)
                            request.setRequestHeader("Content-Type", "application/json");
                            request.onload = () => {
                                    const response = request.responseText;
                                    const json = JSON.parse(response);
                                    //console.log("JSON:", json);
                                    if (request.status == 202) {
                                            alert(json.mensaje);
                                            window.location.replace("/home/");
                                    } 
                                    else if(request.status == 403) {
                                            alert(json.detail);
                                            sessionStorage.clear()
                                            window.location.replace("/")
                                    }
                            }
                            request.send(JSON.stringify(payload));
                    }
                    else {
                            window.location.replace("/");
                    }    
            }
            else {
                   alert("Verifique la dirección de correo ingresada.")
                   document.getElementById("email").focus(); 
            }
    }
}