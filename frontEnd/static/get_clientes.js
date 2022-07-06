function getClienteByID() {
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
   
    request.open('GET', 'https://8000-luisescobar09-apirest-zbeh2r72okr.ws-us51.gitpod.io/clientes/'+id_cliente, true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Basic " + btoa("admin" + ":" + "admin"))
    request.setRequestHeader("Content-Type", "application/json");

    const  tabla   = document.getElementById("tabla_clientes");

    var tblBody = document.createElement("tbody");
    var tblHead = document.createElement("thead");

    tblHead.innerHTML = `
        <tr>
            <th>ID Cliente</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Opciones</th>
        </tr>`;

    request.onload = () => {
        // Almacena la respuesta en una variable, si es 202 es que se obtuvo correctamente
        const response = request.responseText;
        const json = JSON.parse(response);
        console.log("Response " + response);
        console.log("Json " +  json);
        if (request.status === 401 || request.status === 403) {
            alert(json.detail);
            window.location.replace("http://localhost:8080/validate/");
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

                get_cliente.innerHTML = "<a href='\\producto\\get\\"+json.id_cliente+"'>Ver</a>";
                id_cliente.innerHTML = json.id_cliente;
                nombre.innerHTML = json.nombre;
                email.innerHTML = json.email;

                tr.appendChild(id_cliente);
                tr.appendChild(nombre);
                tr.appendChild(email);
                tr.appendChild(get_cliente);
                
                tblBody.appendChild(tr);
                tabla.appendChild(tblHead);
                tabla.appendChild(tblBody);
            }
        }
    }
    request.send();
}

function getClientes(offset) {
    var request = new XMLHttpRequest();
    //Accede a la session de la pagina
    username= sessionStorage.getItem("username");
    password= sessionStorage.getItem("password");
   
    request.open('GET', 'https://8000-luisescobar09-apirest-zbeh2r72okr.ws-us51.gitpod.io/clientes/?offset='+offset+'&limit=10', true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Basic " + btoa("admin" + ":" + "admin"))
    request.setRequestHeader("Content-Type", "application/json");

    const  tabla   = document.getElementById("tabla_clientes");

    var tblBody = document.createElement("tbody");
    var tblHead = document.createElement("thead");

    tblHead.innerHTML = `
        <tr>
            <th>ID Cliente</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Opciones</th>
        </tr>`;

    request.onload = () => {
        // Almacena la respuesta en una variable, si es 202 es que se obtuvo correctamente
        const response = request.responseText;
        const json = JSON.parse(response);
        console.log("Response " + response);
        console.log("Json " +  json);
        if (request.status === 401 || request.status === 403) {
            alert(json.detail);
            window.location.replace("http://localhost:8080/validate/");
        }
        else if (request.status == 202){
            console.log(request);
            const response = request.responseText;
            const json = JSON.parse(response);
            console.log(json);
            for (let i = 0; i < json.length; i++) {
                var tr = document.createElement('tr');
                var get_cliente = document.createElement('td');
                var id_cliente = document.createElement('td');
                var nombre = document.createElement('td');
                var email = document.createElement('td');

                get_cliente.innerHTML = "<a href='\\producto\\get\\"+json[i].id_cliente+"'>Ver</a>";
                id_cliente.innerHTML = json[i].id_cliente;
                nombre.innerHTML = json[i].nombre;
                email.innerHTML = json[i].email;

                tr.appendChild(id_cliente);
                tr.appendChild(nombre);
                tr.appendChild(email);
                tr.appendChild(get_cliente);
                
                tblBody.appendChild(tr);
            }
            tabla.appendChild(tblHead);
            tabla.appendChild(tblBody);
        }
    };
    request.send();
}