function post_cliente() {
    var nombre = document.getElementById("nombre").value;
    var email = document.getElementById("email").value;
    console.log(nombre, email)

    var payload = {
            "nombre" : nombre,
            "email" : email
    }
    var request = new XMLHttpRequest();
    request.open("POST", "http://localhost:8000/clientes/", true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Basic " + btoa("admin" + ":" + "admin"))
    request.setRequestHeader("Content-Type", "application/json");

    request.onload = () => {
            const response = request.responseText;
            const json = JSON.parse(response);
            console.log("JSON:", json);

            if (request.status == 202) {
                    alert(json.mensaje);
                    window.location.replace("/");
            }
    }
    request.send(JSON.stringify(payload));
}