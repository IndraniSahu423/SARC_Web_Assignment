import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { axiosPortal } from "../services/api";

export default function DashboardPage() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;

    const fetchDashboard = async () => {
      try {
        const response = await axiosPortal.get("/api/portal/dashboard/");
        if (isMounted) {
          setData(response.data);
        }
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.removeItem("sarc_token");
          navigate("/login");
          return;
        }
        if (isMounted) {
          setError("Failed to load dashboard.");
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchDashboard();

    return () => {
      isMounted = false;
    };
  }, [navigate]);

  const logout = () => {
    localStorage.removeItem("sarc_token");
    navigate("/login");
  };

  return (
    <div className="page">
      <div className="card">
        <h1>Dashboard</h1>
        {loading ? <p>Loading...</p> : null}
        {error ? <p className="error">{error}</p> : null}

        {data ? (
          <div className="profile-block">
            <p>
              <strong>Name:</strong> {data.name}
            </p>
            <p>
              <strong>Roll Number:</strong> {data.roll_number}
            </p>
          </div>
        ) : null}

        <button onClick={logout} className="secondary-btn">
          Logout
        </button>
      </div>
    </div>
  );
}
