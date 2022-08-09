function logout() {
    token = sessionStorage.getItem('token')
    if (token != null) {
            sessionStorage.clear();
    }
    window.location.replace("/");
}

function get() {
    token = sessionStorage.getItem('token')
    if (token != null) {
            sendRequest(token);
    }
    else {
            window.location.replace("/")
    }
}

function sendRequest(token) {
    var request = new XMLHttpRequest();
    request.open("GET", "http://localhost:8000/users/", true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Bearer " + token)
    request.setRequestHeader("Content-Type", "application/json");

    request.onload = () => {
            const response = request.responseText;
            const json = JSON.parse(response);
            //console.log("JSON:", json);
            if (request.status === 202) {
                    document.getElementById("email_info").innerHTML = "¡Bienvenido " + json.user_data.email + "!"
            }
            else if (request.status === 403) {
                    alert(json.detail)
                    sessionStorage.clear()
                    window.location.replace("/")
            }
    }
    request.send();
}