const BASE_URL = 'http://127.0.0.1:8000';
let token = localStorage.getItem("token") || null;

function setToken(t) {
  token = t;
  localStorage.setItem("token", t);
}

let data = [];
const api = BASE_URL + '/fridge';
let todoIdInEdit = 0;

document.getElementById('add-btn').addEventListener('click', async (e) => {
  e.preventDefault();
  

  const titleInput = document.getElementById('title');
  const descInput = document.getElementById('desc');
  const categoryInput = document.getElementById('category');

  const name = titleInput.value.trim();
  const quantity = Number(descInput.value);
  const category = categoryInput.value;

  if (!name || isNaN(quantity) || !category) {
    alert("Please fill in all fields correctly.");
    return;
  }

  const res = await fetch(api, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + token
    },
    body: JSON.stringify({
      name, quantity, category
    })
  });

  if (res.ok) {
    const newItem = await res.json();
    data.push(newItem);
    renderTodos(data);

    titleInput.value = '';
    descInput.value = '';
    categoryInput.value = '';
  }
});



//edit button in edit modal dialog
document.getElementById('edit-btn').addEventListener('click', async (e) => {
  e.preventDefault();

  const titleInput = document.getElementById('titleEdit');
  const descInput = document.getElementById('descEdit');
  const categoryInput = document.getElementById('categoryEdit');

  const name = titleInput.value.trim();
  const quantity = Number(descInput.value);
  const category = categoryInput.value;

  if (!name || isNaN(quantity) || !category) {
    alert("Please fill in all fields correctly.");
    return;
  }

  const res = await fetch(api + '/' + todoIdInEdit, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + token
    },
    body: JSON.stringify({
      name,
      quantity,
      category
    })
  });

  if (res.ok) {
    const updated = await res.json();

    const item = data.find(x => x.id == todoIdInEdit);
    if (item) {
      item.name = updated.name;
      item.quantity = updated.quantity;
      item.category = updated.category;
    }

    renderTodos(data);
  }
});

//delete a todo
async function deleteTodo(id) {
  const res = await fetch(api + '/' + id, {
    method: "DELETE",
    headers: {
      "Authorization": "Bearer " + token
    }
  });

  if (res.ok) {
    data = data.filter(x => x.id != id);
    renderTodos(data);
  }
}

//set the todo in edit modal dialog
function setTodoInEdit(id) {
  todoIdInEdit = id;
  const todo = data.find(x => x.id == id);

  document.getElementById('titleEdit').value = todo.name;
  document.getElementById('descEdit').value = todo.quantity;
  document.getElementById('categoryEdit').value = todo.category;
}

//render todos
function renderTodos(data) {
  const todoDiv = document.getElementById('todos');
  todoDiv.innerHTML = '';

  const groups = data.reduce((acc, todo) => {
    const category = todo.category || "Uncategorized";

    if (!acc[category]) acc[category] = [];
    acc[category].push(todo);

    return acc;
  }, {});

  Object.keys(groups).forEach(category => {
    todoDiv.innerHTML += `<h3 class="mt-4">${category}</h3>`;

    groups[category]
      .sort((a, b) => b.id - a.id)
      .forEach(x => {
        todoDiv.innerHTML += `
          <div id="todo-${x.id}" class="todo-box">
            <div class="fw-bold fs-4">${x.name}</div>
            <pre class="text-secondary ps-3">${x.quantity}</pre>
            <div>
              <button
                class="edit-btn btn-sm"
                data-bs-toggle="modal"
                data-bs-target="#modal-edit"
                onClick="setTodoInEdit('${x.id}')"
              >
                edit
              </button>

              <button
                class="delete-btn btn-sm"
                onClick="deleteTodo('${x.id}')"
              >
                delete
              </button>
            </div>
          </div>
        `;
      });
  });
}

//getting todos from backend and render them on frontend
async function getAllTodos() {
  if (!token) {
    document.getElementById("todos").innerHTML = "<p>Please login</p>";
    return;
  }

  const res = await fetch(api, {
    headers: {
      "Authorization": "Bearer " + token
    }
  });

  if (!res.ok) return;

  data = await res.json();
  renderTodos(data);
}

async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch(BASE_URL + "/auth/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ username, password })
  });

  if (!res.ok) {
    alert("login failed");
    return;
  }

  const data = await res.json();
  setToken(data.token);
  getAllTodos(); // reload fridge
}

async function signup() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch(BASE_URL + "/auth/signup", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ username, password })
  });

  if (!res.ok) {
    alert("signup failed");
    return;
  }

  const data = await res.json();
  setToken(data.token);
  alert("signup successful");
  getAllTodos();
}

function logout() {
  token = null;
  localStorage.removeItem("token");
  data = [];
  document.getElementById("todos").innerHTML = "<p>Logged out</p>";
}

//init
(() => {
  getAllTodos();
})();