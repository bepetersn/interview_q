import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../App.css";
import api from "../api";

const LoginPage = (props) => {
    const { onLogin } = props || {};
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        try {
            const response = await api.post(
                "accounts/login/",
                { username, password }
            );
            // localStorage.setItem("user", JSON.stringify(response.data));
            onLogin(response.data);
        } catch (err) {
            setError(
                err.response?.data?.detail || err.message || "Login failed."
            );
        }
    };

    return (
        <div className="login-container">
            <form className="login-form" onSubmit={handleSubmit}>
                <h2>Login</h2>
                {error && <div className="error">{error}</div>}
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    autoComplete="username"
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    autoComplete="current-password"
                />
                <button type="submit">Login</button>
                <button
                    type="button"
                    style={{ marginTop: "0.5rem" }}
                    onClick={() => navigate("/register")}
                >
                    Register
                </button>
            </form>
        </div>
    );
};

export default LoginPage;
