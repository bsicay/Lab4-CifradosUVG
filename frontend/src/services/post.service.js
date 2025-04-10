import axios from "axios";
import authHeader from "./auth-header";

const API_URL = "http://127.0.0.1:5000/file";

const getAllFiles = () => {
  return axios.get(`${API_URL}/archivos`, { headers: authHeader() });
};

const downloadFile = (fileId) => {
  return axios.get(`${API_URL}/archivos/${fileId}/descargar`, {
    headers: authHeader(),
  });
};
const uploadFile = (file, privateKey, sign = false) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("private_key", privateKey);

  return axios.post(`${API_URL}/guardar/${sign}`, formData, {
    headers: {
      ...authHeader(),
      "Content-Type": "multipart/form-data",
    },
  });
};

const verifyFile = (file, ownerEmail) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("owner", ownerEmail);

  return axios.post(`${API_URL}/verificar`, formData, {
    headers: {
      ...authHeader(),
      "Content-Type": "multipart/form-data",
    },
  });
};



const postService = {
  getAllFiles,
  downloadFile,
  uploadFile,
  verifyFile
};

export default postService;
