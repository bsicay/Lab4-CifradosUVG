import axios from "axios";

const API_URL = "http://127.0.0.1:5000/auth";


const signup = (email, password) => {
  return axios
    .post(API_URL + "/register", {
      email,
      password,
    })
    .then((response) => {
      if (response.data.access_token && response.data.refresh_token) {
        localStorage.setItem("user", JSON.stringify(response.data));
      }

      return response.data;
    });
};

const login = (email, password) => {
  return axios
    .post(API_URL + "/login", {
      email,
      password
    })
    .then((response) => {
      if (response.data.access_token && response.data.refresh_token) {
        localStorage.setItem("user", JSON.stringify(response.data));
      }

      return response.data;
    });
};

const logout = () => {
  localStorage.removeItem("user");
};

const getCurrentUser = () => {
  return JSON.parse(localStorage.getItem("user"));
};

const authService = {
  signup,
  login,
  logout,
  getCurrentUser,
};

export default authService;
