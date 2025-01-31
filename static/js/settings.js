document.addEventListener('DOMContentLoaded', function() {
  const emailToggleButton = document.getElementById('email-toggle');
  const adminRequestButton = document.getElementById('admin-request');
  const emailNote = document.getElementById('email-note');
  const adminNote = document.getElementById('admin-note');
  const accessToken = sessionStorage.getItem("AccessToken");
  const url = 'https://2tzh9snyml.execute-api.eu-west-1.amazonaws.com/Test';

  const isAdmin = sessionStorage.getItem('groups').includes("Admins");
  let emailNotifications = false;

  // Initial fetch to get email verification status
  const headers = new Headers();
  headers.set('AccessToken', accessToken);
  
fetch(url + '/settings', {
  method: "GET",
  headers: headers,
})
.then(response => response.json())
.then(data => {
  emailNotifications = data.verified;
  console.log(data);
  sessionStorage.setItem('emailNotifications', emailNotifications);
})
.catch(error => console.error('Error fetching email verification status:', error));

  function updateUI() {
      if (isAdmin) {
          emailToggleButton.style.display = 'none';
          emailNote.textContent = "Note: Admins are advised to have notifications on and hence, can't disable email notifications";
      } else {
          emailToggleButton.style.display = 'block';
          if (emailNotifications) {
              emailToggleButton.textContent = 'Disable Email Notifications';
              emailToggleButton.classList.remove('bg-blue-500', 'hover:bg-blue-700');
              emailToggleButton.classList.add('bg-red-500', 'hover:bg-red-700');
              adminRequestButton.disabled = false;
              adminNote.textContent = '';
          } else {
              emailToggleButton.textContent = 'Enable Email Notifications';
              emailToggleButton.classList.remove('bg-red-500', 'hover:bg-red-700');
              emailToggleButton.classList.add('bg-blue-500', 'hover:bg-blue-700');
              adminRequestButton.disabled = true;
              adminNote.textContent = 'Note: You have to enable email notifications to proceed';
              emailNote.textContent = 'Note: An email from AWS will be sent to you to verify your status after agreeing to enable email notifications';
          }
      }
  }

  async function sendRequest(method, action) {
      try {
          const headers = new Headers({
              'Content-Type': 'application/json',
              'Action': action
          });

          const response = await fetch(url + '/settings', {
              method: method,
              headers: headers,
              body: JSON.stringify({ 
                  accessToken: sessionStorage.getItem('AccessToken') 
              })
          });

          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }

          const data = await response.json();
          if (data.status === 'success') {
              emailNotifications = action === 'email-enable';
              sessionStorage.setItem('emailNotifications', emailNotifications);
              updateUI();
          } else {
              alert('Operation failed. Please try again.');
          }
      } catch (error) {
          console.error('Error:', error);
          alert('An error occurred. Please try again.');
      }
  }

  emailToggleButton.addEventListener('click', function() {
      const action = emailNotifications ? 'email-disable' : 'email-enable';
      const method = action === "email-enable" ? "POST" : "DELETE";
      sendRequest(method, action);
  });

  adminRequestButton.addEventListener('click', function() {
      sendRequest("POST", 'admin-request');
  });

  updateUI();
});

function handleLogout() {
  sessionStorage.clear();
  window.location.href = 'index.html';
}