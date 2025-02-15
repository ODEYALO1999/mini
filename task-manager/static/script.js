document.getElementById('taskForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const title = document.getElementById('title').value;
  const description = document.getElementById('description').value;
  const deadline = document.getElementById('deadline').value;
  const priority = document.getElementById('priority').value;

  const response = await fetch('/add_task', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, description, deadline, priority }),
  });

  if (response.ok) {
    alert('Задача добавлена!');
    loadTasks();
  }
});

async function loadTasks() {
  const response = await fetch('/get_tasks');
  const tasks = await response.json();

  const taskList = document.getElementById('taskList');
  taskList.innerHTML = '';

  tasks.forEach((task) => {
    const li = document.createElement('li');
    li.textContent = `${task.title} (Дедлайн: ${task.deadline}, Приоритет: ${task.priority})`;

    const closeButton = document.createElement('button');
    closeButton.textContent = 'Закрыть';
    closeButton.onclick = async () => {
      await fetch(`/close_task/${task.id}`, { method: 'PUT' });
      alert('Задача закрыта!');
      loadTasks();
    };

    li.appendChild(closeButton);
    taskList.appendChild(li);
  });
}

// Загрузка задач при запуске
loadTasks();