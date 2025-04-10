import axios from "axios";
import authHeader from "./auth-header";
const API_URL = "http://127.0.0.1:5000/key";

const generateKeyPair = () => {
//   return axios.get(API_URL + "/generate", { headers: authHeader() });
    return axios.get(`${API_URL}/generate`, {
        headers: authHeader(),
    });
};


const keyService = {
    generateKeyPair,
};

export default keyService;
