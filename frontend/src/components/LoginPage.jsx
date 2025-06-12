import React, { useState, useEffect } from "react";
import "../App.css";
import api from "../api";
import RegisterPage from "./RegisterPage";
import { getCookie } from "../utils.js";

const LoginPage = ({ onLogin }) => {
    const [showRegister, setShowRegister] = useState(false);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    function autoLoginIfPossible() {
        const userData = localStorage.getItem("user");
        const sessionid = getCookie("sessionid");
        if (userData && sessionid) {
            try {
                const user = JSON.parse(userData);
                if (user?.username) {
                    onLogin(user);
                }
            } catch {}
        }
    }

    useEffect(autoLoginIfPossible, [onLogin]);

    if (showRegister) {
        return (
            <RegisterPage
                onRegister={(username) => {
                    setShowRegister(false);
                    setUsername(username);
                }}
            />
        );
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        try {
            const csrftoken = getCookie("csrftoken");
            const response = await api.post(
                "accounts/login/",
                { username, password },
                { headers: { "X-CSRFToken": csrftoken } }
            );
            localStorage.setItem("user", JSON.stringify(response.data));
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
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Login</button>
                <button
                    type="button"
                    style={{ marginTop: "0.5rem" }}
                    onClick={() => setShowRegister(true)}
                >
                    Register
                </button>
            </form>
        </div>
    );
};

export default LoginPage;
