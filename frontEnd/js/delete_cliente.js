function delete_cliente(id_cliente) {
    console.log(id_cliente);
    var request = new XMLHttpRequest();
    request.open("DELETE", "http://localhost:8000/clientes/"+id_cliente, true);
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
    request.send();
}