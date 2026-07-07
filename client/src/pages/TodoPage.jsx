import { useEffect, useState } from "react";
import axios from "axios";
import { Link, useNavigate, useParams } from "react-router-dom";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000/api";

function TodoPage() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [list, setList] = useState(null);
    const [tasks, setTasks] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        const token = localStorage.getItem("token");

        if (!token) {
            navigate("/");
            return;
        }

        async function loadList() {
            try {
                const headers = { Authorization: `Bearer ${token}` };
                const [listResponse, tasksResponse] = await Promise.all([
                    axios.get(`${API_BASE_URL}/lists/${id}`, { headers }),
                    axios.get(`${API_BASE_URL}/tasks`, { headers, params: { list_id: id } }),
                ]);

                setList(listResponse.data.list);
                setTasks(tasksResponse.data.tasks || []);
            } catch (err) {
                setError(err.response?.data?.message || "Failed to load list");
            }
        }

        loadList();
    }, [id, navigate]);

    if (error) {
        return <h1>{error}</h1>;
    }

    if (!list) {
        return <h1>Loading...</h1>;
    }

    return (
        <div>
            <h1>{list.name}</h1>
            <p>
                <Link to="/dashboard">Back to dashboard</Link>
            </p>
            <ul>
                {tasks.map((task) => (
                    <li key={task.id}>
                        {task.title} {task.completed ? "(done)" : ""}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default TodoPage;