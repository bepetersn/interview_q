import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../login.css";
import api from "../api";


const RegisterPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }
    try {
      await api.post(
        "accounts/register/",
        { username, password },
      );
      setSuccess("Registration successful! You can now log in.");
      setTimeout(() => navigate("/"), 1200);
    } catch (err) {
      setError(
        err.response?.data?.detail || err.message || "Registration failed."
      );
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Register</h2>
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
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
        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default RegisterPage;
