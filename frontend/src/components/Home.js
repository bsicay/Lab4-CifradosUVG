import React, { useState, useEffect } from "react";
import AuthService from "../services/auth.service";
import keyService from "../services/key.service";
import postService from "../services/post.service";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const [privatePosts, setPrivatePosts] = useState([]);
  const [currentUser, setCurrentUser] = useState(undefined);
  const [selectedFile, setSelectedFile] = useState(null);
  const [privateKey, setPrivateKey] = useState("");
  const [signFile, setSignFile] = useState(false);
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    const user = AuthService.getCurrentUser();
    if (user) setCurrentUser(user);

    postService.getAllFiles().then(
      (response) => {
        setPrivatePosts(response.data);
      },
      (error) => {
        console.log("Private page", error.response);
        if (error.response && error.response.status === 403) {
          AuthService.logout();
          navigate("/login");
          window.location.reload();
        }
      }
    );
  }, [navigate]);

  const handleKeyDownload = () => {
    keyService.generateKeyPair()
      .then((response) => {
        const { private_key, public_key } = response.data;

        const privateBlob = new Blob([private_key], { type: "text/plain" });
        const privateUrl = URL.createObjectURL(privateBlob);
        const privateLink = document.createElement("a");
        privateLink.href = privateUrl;
        privateLink.download = "private_key.pem";
        privateLink.click();
        URL.revokeObjectURL(privateUrl);

        const publicBlob = new Blob([public_key], { type: "text/plain" });
        const publicUrl = URL.createObjectURL(publicBlob);
        const publicLink = document.createElement("a");
        publicLink.href = publicUrl;
        publicLink.download = "public_key.pem";
        publicLink.click();
        URL.revokeObjectURL(publicUrl);
      })
      .catch((error) => {
        console.error("Error al generar las llaves:", error);
        alert("No se pudieron generar las llaves.");
      });
  };

  const handlePrivateKeyUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setPrivateKey(e.target.result);
      };
      reader.readAsText(file);
    }
  };
  

  const handleUpload = () => {
    if (!selectedFile || !privateKey) {
      setMessage("Por favor selecciona un archivo y pega tu clave privada.");
      return;
    }

    postService.uploadFile(selectedFile, privateKey, signFile)
      .then((response) => {
        setMessage(`Archivo subido exitosamente: ${response.data.filename}`);
      })
      .catch((error) => {
        console.error("Error al subir archivo:", error);
        setMessage("Error al subir archivo.");
      });
  };

  return (
    <div className="container text-center mt-5">
      {currentUser && (
        <>
          <h1 className="display-4 mb-4">Bienvenido</h1>
          <button className="btn btn-primary mb-4" onClick={handleKeyDownload}>
            Generar par de llaves
          </button>

          <h4 className="mb-3">Cargar archivo</h4>
          <div className="mb-2">
            <input
              type="file"
              onChange={(e) => setSelectedFile(e.target.files[0])}
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Cargar clave privada (.pem):</label>
            <input
              type="file"
              accept=".pem,.txt"
              className="form-control"
              onChange={handlePrivateKeyUpload}
            />
          </div>

          <div className="form-check mb-3">
            <input
              type="checkbox"
              className="form-check-input"
              checked={signFile}
              onChange={() => setSignFile(!signFile)}
              id="signCheckbox"
            />
            <label className="form-check-label" htmlFor="signCheckbox">
              Firmar archivo digitalmente
            </label>
          </div>
          <button className="btn btn-success mb-4" onClick={handleUpload}>
            Upload
          </button>

          {message && <div className="alert alert-info mt-3">{message}</div>}
        </>
      )}

      <h3>Archivos</h3>
      {privatePosts.map((post, index) => (
        <div key={index}>
          {post.filename} {post.is_signed ? "(Firmado)" : ""}
        </div>
      ))}
    </div>
  );
};

export default Home;
