import axios from "axios";

const authBaseUrl = import.meta.env.VITE_AUTH_URL;
const portalBaseUrl = import.meta.env.VITE_PORTAL_URL;

export const axiosAuth = axios.create({
  baseURL: authBaseUrl,
});

export const axiosPortal = axios.create({
  baseURL: portalBaseUrl,
});

axiosPortal.interceptors.request.use((config) => {
  const token = localStorage.getItem("sarc_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

axiosPortal.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("sarc_token");
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);
