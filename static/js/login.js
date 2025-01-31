document.getElementById('loginForm').addEventListener('submit', async function(event) {
  event.preventDefault();
  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const url = 'https://2tzh9snyml.execute-api.eu-west-1.amazonaws.com/Test';
  const raw = JSON.stringify({
      "username": username,
      "password": password
  });
  const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: raw,
      redirect: "follow",
  };
  const response = await fetch(url + '/users/login', requestOptions)
  if (response.ok) {
      const data = await response.json();
      sessionStorage.setItem('username', username);
      sessionStorage.setItem('groups', data.Groups);
      sessionStorage.setItem('IdToken', data.AuthenticationResult.IdToken);
      sessionStorage.setItem('AccessToken', data.AuthenticationResult.AccessToken);
      if (data.Groups.includes('Admins')) {
          window.location.href = 'admin.html';
      } else if (data.Groups.includes('Members')) {
          window.location.href = 'member.html';
      } else {
          window.location.href = 'index.html';
      }
  } else {
      alert('Login failed');
      console.log(response)
  }
});