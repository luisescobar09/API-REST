function delete_cliente(id_cliente) {
    token = sessionStorage.getItem('token')
    if (token != null) {
            var request = new XMLHttpRequest();
            request.open("DELETE", "http://localhost:8000/clientes/"+id_cliente, true);
            request.setRequestHeader("Accept", "application/json");
            request.setRequestHeader("Authorization", "Bearer " + token)
            request.setRequestHeader("Content-Type", "application/json");

            request.onload = () => {
                    const response = request.responseText;
                    const json = JSON.parse(response);
                    console.log("JSON:", json);

                    if (request.status == 202) {
                            alert(json.mensaje);
                            window.location.replace("/home/");
                    }
            }
            request.send();
    }
    else {
            window.location.replace("/");
    }
}