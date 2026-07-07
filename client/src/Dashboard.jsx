import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";

const initialLists = [
  {
    id: 1,
    name: "Groceries",
    tasks: [
      { id: 1, title: "Snacks", done: false, tags: ["important", "time-sensitive"] },
      { id: 2, title: "Vegetables", done: false, tags: ["healthy", "time-sensitive"] },
    ],
  },
  {
    id: 2,
    name: "My Second List",
    tasks: [
      { id: 3, title: "Laundry", done: true, tags: ["healthy"] },
      { id: 4, title: "Pay bills", done: false, tags: ["important"] },
      { id: 5, title: "Call plumber", done: false, tags: [] },
      { id: 6, title: "Read book", done: false, tags: [] },
      { id: 7, title: "Water plants", done: false, tags: ["time-sensitive"] },
    ],
  },
];

function Dashboard() {
  const navigate = useNavigate();
  const [lists, setLists] = useState(initialLists);
  const [selectedListId, setSelectedListId] = useState(initialLists[0].id);
  const [newTaskText, setNewTaskText] = useState("");
  const user = JSON.parse(localStorage.getItem("user") || "null");

  const currentList = lists.find((list) => list.id === selectedListId) || lists[0];
  const totalTasks = currentList.tasks.length;
  const completedTasks = currentList.tasks.filter((task) => task.done).length;
  const pendingTasks = totalTasks - completedTasks;
  const noTagCount = currentList.tasks.filter((task) => task.tags.length === 0).length;
  const tagCounts = currentList.tasks.reduce((counts, task) => {
    task.tags.forEach((tag) => {
      counts[tag] = (counts[tag] || 0) + 1;
    });
    return counts;
  }, {});

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/");
  }

  function handleAddList() {
    const listName = prompt("Enter a name for the new list:");
    if (!listName) return;

    setLists([
      ...lists,
      {
        id: Date.now(),
        name: listName,
        tasks: [],
      },
    ]);
  }

  function handleRenameList() {
    const newName = prompt("Rename list:", currentList.name);
    if (!newName) return;

    setLists(
      lists.map((list) =>
        list.id === selectedListId ? { ...list, name: newName } : list
      )
    );
  }

  function handleAddTask() {
    if (!newTaskText.trim()) return;

    setLists(
      lists.map((list) => {
        if (list.id !== selectedListId) return list;

        return {
          ...list,
          tasks: [
            ...list.tasks,
            {
              id: Date.now(),
              title: newTaskText,
              done: false,
              tags: [],
            },
          ],
        };
      })
    );

    setNewTaskText("");
  }

  function handleToggleTask(taskId) {
    setLists(
      lists.map((list) => {
        if (list.id !== selectedListId) return list;

        return {
          ...list,
          tasks: list.tasks.map((task) =>
            task.id === taskId ? { ...task, done: !task.done } : task
          ),
        };
      })
    );
  }

  function handleOpenTodoPage() {
    navigate(`/todo/${selectedListId}`);
  }

  return (
    <div className="app">
      <header className="topbar">
        <h1>Todo App</h1>
        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </header>

      <div className="main-content">
        <aside className="sidebar">
          <div className="user-name">{user?.name || "Vignesh Kumar"}</div>
          <p className="section-title">MY LISTS</p>

          {lists.map((list) => (
            <div
              key={list.id}
              className={list.id === selectedListId ? "list-item active" : "list-item"}
              onClick={() => setSelectedListId(list.id)}
            >
              <span>{list.name}</span>
              <span className="count">{list.tasks.length}</span>
            </div>
          ))}

          <div className="add-list-btn" onClick={handleAddList}>
            + New List
          </div>
        </aside>

        <main className="tasks-panel">
          <div className="tasks-header">
            <h2>
              {currentList.name}
              <button className="edit-btn" onClick={handleRenameList}>
                ✎
              </button>
            </h2>

            <div className="add-task-box">
              <input
                type="text"
                placeholder="New task..."
                value={newTaskText}
                onChange={(e) => setNewTaskText(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") handleAddTask();
                }}
              />
              <button onClick={handleAddTask}>+ New Task</button>
            </div>
          </div>

          <div className="task-list">
            {currentList.tasks.length === 0 ? (
              <p className="empty-msg">No tasks in this list yet.</p>
            ) : (
              currentList.tasks.map((task) => (
                <div className="task-row" key={task.id}>
                  <input
                    type="checkbox"
                    checked={task.done}
                    onChange={() => handleToggleTask(task.id)}
                  />
                  <div>
                    <p className={task.done ? "task-done" : ""}>{task.title}</p>
                    {task.tags.length > 0 && (
                      <div className="tags">
                        {task.tags.map((tag) => (
                          <span className="tag" key={tag}>
                            #{tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>

          <button className="open-full-page-btn" onClick={handleOpenTodoPage}>
            Open full list page
          </button>
        </main>

        <aside className="stats-panel">
          <p className="section-title">LIST STATISTICS</p>

          <div className="stat-row">
            <span>Total Tasks</span>
            <span>{totalTasks}</span>
          </div>
          <div className="stat-row">
            <span>Pending</span>
            <span className="pending">{pendingTasks}</span>
          </div>
          <div className="stat-row">
            <span>Completed</span>
            <span className="completed">{completedTasks}</span>
          </div>

          <hr />

          {Object.keys(tagCounts).map((tag) => (
            <div className="stat-row" key={tag}>
              <span>#{tag}</span>
              <span>{tagCounts[tag]}</span>
            </div>
          ))}

          <div className="stat-row">
            <span>No Tag</span>
            <span>{noTagCount}</span>
          </div>
        </aside>
      </div>
    </div>
  );
}

export default Dashboard;
