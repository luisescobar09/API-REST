function getCliente() {
    token = sessionStorage.getItem('token')

    if (token != null) {
        var id_cliente = window.location.search.substring(1);
        var request = new XMLHttpRequest();
        //Accede a la session de la pagina
        username= sessionStorage.getItem("username");
        password= sessionStorage.getItem("password");
       
        request.open('GET', 'http://localhost:8000/clientes/'+id_cliente, true);
        request.setRequestHeader("Accept", "application/json");
        request.setRequestHeader("Authorization", "Bearer " + token)
        request.setRequestHeader("Content-Type", "application/json");
    
        request.onload = () => {
            // Almacena la respuesta en una variable, si es 202 es que se obtuvo correctamente
            const response = request.responseText;
            const json = JSON.parse(response);
            if (request.status === 401 || request.status === 403) {
                alert(json.detail);
                sessionStorage.clear()
                window.location.replace("/")
            }
            else if (request.status == 202){
                console.log(request);
                const response = request.responseText;
                const json = JSON.parse(response);
                console.log(json);
                var id_cliente = document.getElementById('id_cliente');
                var nombre = document.getElementById('nombre');
                var email = document.getElementById('email');

                id_cliente.value = json.id_cliente;
                nombre.value = json.nombre;
                email.value = json.email;
            }
            else if (request.status == 404) {
                const errorID = '<div class="alert alert-danger d-flex align-items-center text-center" role="alert"><svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>Ningun resultado coincide con su busqueda.</div></div>'
                window.location.replace("/home/error/");
            }
        }
        request.send();
    }
    else {
        window.location.replace("/");
    }
}