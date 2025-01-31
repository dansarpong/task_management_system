document.addEventListener('DOMContentLoaded', function() {
    const tasksContainer = document.getElementById('tasks-container');
    const noTasksMessage = document.getElementById('no-tasks-message');
    const idToken = sessionStorage.getItem('IdToken');
    const username = sessionStorage.getItem('username');
    const url = 'https://2tzh9snyml.execute-api.eu-west-1.amazonaws.com/Test';
    const headers = new Headers();
    headers.append("Token", idToken);
    headers.append("Member", username);

    // Fetch tasks for the member
    fetch(url + '/tasks', {
        method: 'GET',
        headers: headers,
        redirect: "follow",
    })
    .then(response => response.json())
    .then(data => {
        if (data.length === 0) {
          noTasksMessage.classList.remove('hidden');
        } else {
          noTasksMessage.classList.add('hidden');
          data.forEach(task => {
            // remove if you figure out why it shows all tasks instead of
                if (task.assignee.S !== username) {
                    return;
                }
                const taskElement = document.createElement('div');
                taskElement.className = 'bg-white shadow-md rounded p-6 mb-4';
                taskElement.innerHTML = `
                    <form method="POST" action="/update_task/${task.id.N}">
                        <div class="form-group mb-4">
                            <label for="name" class="block text-gray-700">Task Name:</label>
                            <input type="text" name="name" value="${task.name.S}" readonly class="mt-1 block w-full border-gray-500 rounded-md shadow-sm bg-gray-100 p-2">
                        </div>
                        <div class="form-group mb-4">
                            <label for="deadline" class="block text-gray-700">Deadline:</label>
                            <input type="date" name="deadline" value="${task.deadline.S !== 'none' ? task.deadline.S : ""}" class="mt-1 block w-full border-gray-500 rounded-md shadow-sm p-2" disabled>
                        </div>
                        <div>
                            <label for="assignee">Assignee:</label>
                            <input type="text" name="assignee" value="${task.assignee.S}" class="mt-1 block w-full border-gray-500 rounded-md shadow-sm p-2">
                        </div>
                        <div class="form-group mb-4">
                            <label for="status" class="block text-gray-700">Status:</label>
                            <select name="status" class="mt-1 block w-full border-gray-500 rounded-md shadow-sm p-2">
                                <option value="pending" ${task.status.S === 'pending' ? 'selected' : ''}>pending</option>
                                <option value="ongoing" ${task.status.S === 'ongoing' ? 'selected' : ''}>ongoing</option>
                                <option value="completed" ${task.status.S === 'completed' ? 'selected' : ''}>completed</option>
                            </select>
                        </div>
                        <button type="submit" class="bg-blue-500 text-white py-2 px-4 rounded" title="Update Task">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                            </svg>
                        </button>
                    </form>
                `;
                tasksContainer.appendChild(taskElement);
            });
        }
    })
    .catch(error => console.error('Error fetching tasks:', error));
});

function handleLogout() {
    sessionStorage.clear();
    window.location.href = 'index.html';
}
