document.addEventListener('DOMContentLoaded', function() {
    const username = sessionStorage.getItem('username');
    const idToken = sessionStorage.getItem('IdToken');
    const groups = sessionStorage.getItem('groups');

    if (username && idToken && groups) {
        if (groups.includes('Admins')) {
            window.location.href = 'admin.html';
        } else if (groups.includes('Members')) {
            window.location.href = 'member.html';
        }
    }
});
