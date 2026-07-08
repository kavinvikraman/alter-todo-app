# 📝 Todo Management Application

A full-stack **Todo Management Application** built using **React**, **Python Flask**, and **MongoDB**. The application allows users to securely create and manage multiple todo lists, organize tasks, monitor task progress, and share todo lists through public links.

---

# 📌 Project Overview

The Todo Management Application helps users organize and manage their daily tasks efficiently. Users can create multiple todo lists, add tasks to each list, update task status, and track overall progress. The application follows a client-server architecture where the React frontend communicates with a Flask backend using REST APIs, while MongoDB stores all application data.

---

# ✨ Features

## 🔐 User Authentication
- User Registration (Sign Up)
- Secure Login
- JWT Authentication
- Password Encryption using Bcrypt

## 📋 Todo List Management
- Create Multiple Todo Lists
- Rename Todo Lists
- Delete Todo Lists
- View All Todo Lists

## ✅ Task Management
- Add New Tasks
- Edit Tasks
- Delete Tasks
- Mark Tasks as Completed or Pending

## 🏷️ Task Tags
- Assign Tags to Tasks

## 📊 Statistics
Each Todo List displays:
- Total Tasks
- Completed Tasks
- Pending Tasks
- Number of Tasks for Each Tag

## 🔗 Public Todo List Sharing
- Generate a Unique Public Share Link
- View Shared Todo Lists in Read-Only Mode

---

# 🏗️ System Architecture

```
React Frontend
        │
        │ REST API (Axios)
        ▼
Python Flask Backend
        │
        │ PyMongo
        ▼
MongoDB Database
```

---

# 🛠️ Tech Stack

## Frontend
- React.js
- React Router DOM
- Axios
- HTML5
- CSS3
- JavaScript (ES6)

## Backend
- Python
- Flask
- Flask-CORS
- PyMongo
- JWT Authentication
- Bcrypt
- Python Dotenv

## Database
- MongoDB

---

# 📂 Project Structure

```
Todo-App
│
├── client
│   ├── public
│   ├── src
│   │
│   ├── components
│   ├── pages
│   ├── services
│   ├── App.jsx
│   └── main.jsx
│
└── backend
    ├── app.py
    ├── db.py
    ├── auth_utils.py
    ├── requirements.txt
    ├── .env
    │
    └── routes
        ├── auth.py
        ├── lists.py
        ├── tasks.py
        └── share.py
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/your-username/todo-management-app.git
```

## Frontend

```bash
cd client
npm install
npm run dev
```

## Backend

```bash
cd backend

python -m venv venv

# Activate Virtual Environment

Windows
venv\Scripts\activate

Linux / macOS
source venv/bin/activate

pip install -r requirements.txt

python app.py
```

---

# 🌐 Environment Variables

Create a `.env` file inside the backend folder.

```env
MONGO_URI=your_mongodb_connection_string
JWT_SECRET=your_secret_key
PORT=5000
```

---

# 📡 API Endpoints

## Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/auth/signup | Register User |
| POST | /api/auth/login | Login User |

## Todo Lists

| Method | Endpoint |
|---------|----------|
| GET | /api/lists |
| POST | /api/lists |
| PUT | /api/lists/:id |
| DELETE | /api/lists/:id |

## Tasks

| Method | Endpoint |
|---------|----------|
| GET | /api/tasks/:listId |
| POST | /api/tasks |
| PUT | /api/tasks/:id |
| DELETE | /api/tasks/:id |

## Share

| Method | Endpoint |
|---------|----------|
| POST | /api/share |
| GET | /api/share/:shareId |

---

# 📊 Database Collections

## Users

- Name
- Email
- Password (Hashed)

## Todo Lists

- Title
- User ID
- Share ID
- Public Status

## Tasks

- Task Name
- Tag
- Completed Status
- List ID

---



# 👨‍💻 Developed By

**Kavin Vikraman**
