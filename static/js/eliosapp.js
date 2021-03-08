
function post_call(url, data, callback, callnow) {
    let csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value

    console.log(url, data, csrf, callback, callnow);
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

    console.log(params);
    xhr.open('POST', url, true);
    xhr.setRequestHeader("X-CSRFToken", csrf);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("Content-length", params.length);
    xhr.setRequestHeader("Connection", "close");
    xhr.send(params);
    console.log("end of post_call()");
}


function update_habit(data) {
    console.log(data);
}