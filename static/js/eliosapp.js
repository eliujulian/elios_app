
function post_call(url, data, callback) {
    let csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value

    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            data = JSON.parse(xhr.responseText);
            if (callback) {callback(data);}
        }
    };

    let params = "";
    for (const [key, value] of Object.entries(data)) {
        params += key
        params +="="
        params += value
        params += "&"
    }

    xhr.open('POST', url, true);
    xhr.setRequestHeader("X-CSRFToken", csrf);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("Content-length", params.length);
    xhr.setRequestHeader("Connection", "close");
    xhr.send(params);
}


function update_habit(data) {
    let el = document.getElementById(data['id_slug']);
    let streak = document.getElementById(data['id_slug'] + "-current_streak");
    let new_streak = data['current_streak'];
    streak.innerHTML = "Reihe: " + new_streak.toString();
    btns = el.getElementsByClassName("btn");
    var i;
    for (i = 0; i < btns.length; i++) {
        btns[i].disabled = true;
    }
    if (data['last_day_action'] === 1) {
        btns[0].classList.remove("btn-outline-primary");
        btns[0].classList.add("btn-primary");
    }
    if (data['last_day_action'] === 2) {
        btns[1].classList.remove("btn-outline-primary");
        btns[1].classList.add("btn-primary");
    }
    if (data['last_day_action'] === 3) {
        btns[2].classList.remove("btn-outline-primary");
        btns[2].classList.add("btn-primary");
    }
}