import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { axiosPortal } from "../services/api";

export default function RegisterPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    name: "",
    roll_number: "",
    hostel_number: "",
    password: "",
  });
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
      await axiosPortal.post("/api/portal/register/", formData);
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="card">
        <h1>Create Account</h1>
        <p className="subtitle">Register once for SARC services.</p>
        <form onSubmit={onSubmit} className="form">
          <label htmlFor="username">Username</label>
          <input id="username" name="username" value={formData.username} onChange={onChange} required />

          <label htmlFor="name">Name</label>
          <input id="name" name="name" value={formData.name} onChange={onChange} required />

          <label htmlFor="roll_number">Roll Number</label>
          <input id="roll_number" name="roll_number" value={formData.roll_number} onChange={onChange} required />

          <label htmlFor="hostel_number">Hostel Number</label>
          <input id="hostel_number" name="hostel_number" value={formData.hostel_number} onChange={onChange} required />

          <label htmlFor="password">Password</label>
          <input id="password" name="password" type="password" value={formData.password} onChange={onChange} required />

          {error ? <p className="error">{error}</p> : null}

          <button type="submit" disabled={loading}>
            {loading ? "Registering..." : "Register"}
          </button>
        </form>

        <p className="footer-text">
          Already registered? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
}
