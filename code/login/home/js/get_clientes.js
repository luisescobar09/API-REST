function getClienteByID() {
    token = sessionStorage.getItem('token')
    var Parent = document.getElementById("tabla_clientes");
    while(Parent.hasChildNodes()) {
        Parent.removeChild(Parent.firstChild);
    }
    var id_cliente = document.getElementById("input_id_cliente").value;
    //window.location.href = "https://8080-luisescobar09-apirest-zbeh2r72okr.ws-us47.gitpod.io/"+id_cliente;
    console.log(id_cliente);
    var request = new XMLHttpRequest();
    //Accede a la session de la pagina
    username= sessionStorage.getItem("username");
    password= sessionStorage.getItem("password");
   
    request.open('GET', 'http://localhost:8000/clientes/'+id_cliente, true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Bearer " + token)
    request.setRequestHeader("Content-Type", "application/json");

    const  tabla   = document.getElementById("tabla_clientes");

    var tblBody = document.createElement("tbody");
    var tblHead = document.createElement("thead");

    tblHead.innerHTML = `
        <tr>
            <th>ID Cliente</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Ver</th>
            <th>Actualizar</th>
            <th>Borrar</th>
        </tr>`;

    request.onload = () => {
        // Almacena la respuesta en una variable, si es 202 es que se obtuvo correctamente
        const response = request.responseText;
        const json = JSON.parse(response);
        console.log("Response " + response);
        console.log("Json " +  json);
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
            if (json.message == "ID no encontrado") {
                const errorID = '<div class="alert alert-danger d-flex align-items-center text-center" role="alert"><svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>Ningun resultado coincide con su busqueda.</div></div>'
                document.getElementById("alert").innerHTML = errorID;
            }
            else {
                //document.getElementById("alerta").innerHTML = '.';
                var tr = document.createElement('tr');
                var get_cliente = document.createElement('td');
                var id_cliente = document.createElement('td');
                var nombre = document.createElement('td');
                var email = document.createElement('td');
                var get_cliente = document.createElement('td');
                var update_cliente = document.createElement('td');
                var delete_cliente = document.createElement('td');

                get_cliente.innerHTML = "<a class='btn btn-link link-success' href='get\\?"+json.id_cliente+"'><i class='fas fa-eye'></i></a>";
                update_cliente.innerHTML = "<a class='btn btn-link link-info' href='put\\?"+json.id_cliente+"'><i class='far fa-edit'></i></a>";
                delete_cliente.innerHTML = "<a class='btn btn-link link-danger' href='/' onclick='delete_cliente("+json.id_cliente+")'><i class='far fa-trash-alt'></i></a>";
                id_cliente.innerHTML = json.id_cliente;
                nombre.innerHTML = json.nombre;
                email.innerHTML = json.email;

                tr.appendChild(id_cliente);
                tr.appendChild(nombre);
                tr.appendChild(email);
                tr.appendChild(get_cliente);
                tr.appendChild(update_cliente);
                tr.appendChild(delete_cliente);
                
                tblBody.appendChild(tr);
                tabla.appendChild(tblHead);
                tabla.appendChild(tblBody);
            }
        }
    }
    request.send();
}

function getClientes(offset) {
    token = sessionStorage.getItem('token')
    var request = new XMLHttpRequest();
    //Accede a la session de la pagina
    username= sessionStorage.getItem("username");
    password= sessionStorage.getItem("password");
   
    request.open('GET', 'http://localhost:8000/clientes/?offset='+offset+'&limit=20', true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Bearer " + token)
    request.setRequestHeader("Content-Type", "application/json");

    const  tabla   = document.getElementById("tabla_clientes");

    var tblBody = document.createElement("tbody");
    var tblHead = document.createElement("thead");

    tblHead.innerHTML = `
        <tr>
            <th>ID Cliente</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Ver</th>
            <th>Editar</th>
            <th>Borrar</th>
        </tr>`;

    request.onload = () => {
        // Almacena la respuesta en una variable, si es 202 es que se obtuvo correctamente
        const response = request.responseText;
        const json = JSON.parse(response);
        console.log("Response " + response);
        console.log("Json " +  json);
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
            for (let i = 0; i < json.length; i++) {
                var tr = document.createElement('tr');
                var id_cliente = document.createElement('td');
                var nombre = document.createElement('td');
                var email = document.createElement('td');
                var get_cliente = document.createElement('td');
                var update_cliente = document.createElement('td');
                var delete_cliente = document.createElement('td');

                get_cliente.innerHTML = "<a class='btn btn-link link-success' href='get\\?"+json[i].id_cliente+"'><i class='fas fa-eye'></i></a>";
                update_cliente.innerHTML = "<a class='btn btn-link link-info' href='put\\?"+json[i].id_cliente+"'><i class='far fa-edit'></i></a>";
                delete_cliente.innerHTML = "<button type='button' class='btn btn-link link-danger' onclick='delete_cliente("+json[i].id_cliente+")'><i class='far fa-trash-alt'></i></button>";
                id_cliente.innerHTML = json[i].id_cliente;
                nombre.innerHTML = json[i].nombre;
                email.innerHTML = json[i].email;

                tr.appendChild(id_cliente);
                tr.appendChild(nombre);
                tr.appendChild(email);
                tr.appendChild(get_cliente);
                tr.appendChild(update_cliente);
                tr.appendChild(delete_cliente);
                
                tblBody.appendChild(tr);
            }
            tabla.appendChild(tblHead);
            tabla.appendChild(tblBody);
        }
    };
    request.send();
}