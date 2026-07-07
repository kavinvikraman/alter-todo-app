import { useEffect, useState } from "react";
import axios from "axios";
import { Link, useParams } from "react-router-dom";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000/api";

function SharePage() {
    const { id } = useParams();
    const [list, setList] = useState(null);
    const [tasks, setTasks] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadSharedList() {
            try {
                const response = await axios.get(`${API_BASE_URL}/share/${id}`);
                setList(response.data.list);
                setTasks(response.data.tasks || []);
            } catch (err) {
                setError(err.response?.data?.message || "Failed to load shared list");
            }
        }

        loadSharedList();
    }, [id]);

    if (error) {
        return <h1>{error}</h1>;
    }

    if (!list) {
        return <h1>Loading shared list...</h1>;
    }

    return (
        <div>
            <h1>{list.name}</h1>
            <p>
                <Link to="/">Back to login</Link>
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

export default SharePage;