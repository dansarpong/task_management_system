document.addEventListener('DOMContentLoaded', async function() {
    const tasksContainer = document.getElementById('tasks-container');
    const usersCreate = document.getElementById('populate-assignee');
    const noTasksMessage = document.getElementById('no-tasks-message');
    const idToken = sessionStorage.getItem('IdToken');
    // let users = [];
    const usersSelect = document.createElement('select');
    usersSelect.name = "assignee";
    usersSelect.classList.add("mt-1", "block", "w-full", "border-gray-300","rounded-md", "shadow-sm");
    const url = 'https://2tzh9snyml.execute-api.eu-west-1.amazonaws.com/Test';
    const headers = new Headers();
    headers.append("Token", idToken);

    // Fetch users
    await fetch(url + '/users', {
        method: 'GET',
        headers: headers,
        redirect: "follow"
    })
    .then(response => response.json())
    .then(data => {
        data.forEach(user => {
            const option = document.createElement('option');
            option.value = user.username;
            option.textContent = user.username;
            usersSelect.appendChild(option);
        });
        usersCreate.appendChild(usersSelect.cloneNode(true));
    })
    .catch(error => console.error('Error fetching users:', error));

    // Fetch and populate tasks
    fetch(url + '/tasks', {
        method: 'GET',
        headers: headers,
        redirect: "follow"
    })
    .then(response => response.json())
    .then(data => {
        if (data.length === 0) {
            noTasksMessage.classList.remove('hidden');
        } else {
            noTasksMessage.classList.add('hidden');
            data.forEach(task => {
                const taskElement = document.createElement('div');
                taskElement.className = 'bg-white shadow-md rounded p-6 mb-4';
                taskElement.innerHTML = `
                    <form class="w-full" method="POST" action="/update_task/${task.id.N}">
                        <div class="form-group mb-4">
                            <label for="name" class="block text-gray-700">Task Name:</label>
                            <input type="text" name="name" value="${task.name.S}" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm">
                        </div>
                        <div class="form-group mb-4">
                            <label for="deadline" class="block text-gray-700">Deadline:</label>
                            <input type="date" name="deadline" value="${task.deadline.S !== 'none' ? task.deadline.S : ""}" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm">
                        </div>
                        <div class="form-group mb-4">
                            <label for="assignee" class="block text-gray-700">Assigned To:</label>
                        </div>
                        <div class="form-group mb-4">
                            <label for="status" class="block text-gray-700">Status:</label>
                            <select name="status" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm">
                                <option value="pending" ${task.status.S === 'pending' ? 'selected' : ''}>pending</option>
                                <option value="ongoing" ${task.status.S === 'ongoing' ? 'selected' : ''}>ongoing</option>
                                <option value="completed" ${task.status.S === 'completed' ? 'selected' : ''}>completed</option>
                            </select>
                        </div>
                        <div class="flex items-end mb-4">
                            <button type="submit" class="bg-blue-500 text-white py-2 px-4 rounded mr-2" title="Update Task">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                                </svg>
                            </button>
                    </form>
                        <form method="POST" action="/delete_task/${task.id.N}">
                            <button type="submit" class="bg-red-500 text-white py-2 px-4 rounded" title="Delete Task">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6h18M9 6v12m6-12v12M4 6l1 14a2 2 0 002 2h10a2 2 0 002-2l1-14"/>
                                </svg>
                            </button>
                        </form>
                    </div>
                `;
                const taskAssigneeSelect = usersSelect.cloneNode(true);
                Array.from(taskAssigneeSelect.options).forEach(option => {
                    if (option.value === task.assignee.S) {
                        option.selected = true;
                    }
                });
                taskElement.querySelector('div.form-group:nth-child(3)').appendChild(taskAssigneeSelect);
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
