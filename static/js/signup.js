function handleSignup(event) {
    event.preventDefault();

    var username = document.getElementById('username').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirm-password').value;

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return false;
    }
    
    const url = 'https://2tzh9snyml.execute-api.eu-west-1.amazonaws.com/Test';
    var payload = JSON.stringify({
        "username": username,
        "email": email,
        "password": password
    });
    const headers = new Headers();
    headers.append('Content-Type', 'application/json');

    fetch(url + '/users/signup', {
        method: 'POST',
        headers: headers,
        body: payload
    })
    .then(response => response.json())
    .then(data => {
        if (data) {
            sessionStorage.setItem('username', username);
            sessionStorage.setItem('email', email);
            window.location.href = 'confirm.html';
        } else {
            alert("Signup failed: " + data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred:", error);
    });

    return false;
}
