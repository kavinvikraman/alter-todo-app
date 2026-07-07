import { Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./Dashboard";
import TodoPage from "./pages/TodoPage";
import SharePage from "./pages/SharePage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/todo/:id" element={<TodoPage />} />
      <Route path="/share/:id" element={<SharePage />} />
    </Routes>
  );
}

export default App;