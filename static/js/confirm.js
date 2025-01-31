function handleConfirm(event) {
    event.preventDefault();

    var confirmationCode = document.getElementById('code').value;
    var username = sessionStorage.getItem('username');
    var email = sessionStorage.getItem('email');

    if (!username || !email) {
        alert("Session expired. Please sign up again.");
        window.location.href = 'signup.html';
        return false;
    }

    const url = 'https://2tzh9snyml.execute-api.eu-west-1.amazonaws.com/Test';
    var payload = JSON.stringify({
        "username": username,
        "email": email,
        "confirmation_code": confirmationCode
    });
    const headers = new Headers();
    headers.append('Content-Type', 'application/json');

    fetch(url + '/users/signup/confirm', {
        method: 'POST',
        headers: headers,
        body: payload
    })
    .then(response => response.json())
    .then(data => {
        if (data) {
            sessionStorage.clear();
            window.location.href = 'login.html';
        } else {
            alert("Confirmation failed: " + data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred:", error);
    });

    return false;
}
