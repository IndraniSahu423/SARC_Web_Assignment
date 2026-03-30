import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { axiosAuth } from "../services/api";

export default function LoginPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const onSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await axiosAuth.post("/api/auth/login/", formData);
      localStorage.setItem("sarc_token", response.data.access_token);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || err.response?.data?.non_field_errors?.[0] || "Login failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="card">
        <h1>SARC SSO Login</h1>
        <p className="subtitle">Sign in with your centralized account.</p>
        <form onSubmit={onSubmit} className="form">
          <label htmlFor="username">Username</label>
          <input id="username" name="username" value={formData.username} onChange={onChange} required />

          <label htmlFor="password">Password</label>
          <input id="password" name="password" type="password" value={formData.password} onChange={onChange} required />

          {error ? <p className="error">{error}</p> : null}

          <button type="submit" disabled={loading}>
            {loading ? "Signing in..." : "Login"}
          </button>
        </form>

        <p className="footer-text">
          No account? <Link to="/register">Register</Link>
        </p>
      </div>
    </div>
  );
}
