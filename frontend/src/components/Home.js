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
  const [fileToVerify, setFileToVerify] = useState(null);
  const [ownerEmail, setOwnerEmail] = useState("");
  const [verifyResult, setVerifyResult] = useState("");
  const [algorithm, setAlgorithm] = useState("rsa");

  const navigate = useNavigate();

  useEffect(() => {
    const user = AuthService.getCurrentUser();
    if (user) setCurrentUser(user);
    fetchFiles();
  }, [navigate]);

  const fetchFiles = () => {
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
  };

  const handleKeyDownload = () => {
    /*
      Llamamos al servicio de llaves pero
      pasándole el algoritmo que se seleccionó
    */
    keyService.generateKeyPair(algorithm)
      .then((response) => {
        const { private_key, public_key } = response.data;

        // Descargamos la clave privada
        const privateBlob = new Blob([private_key], { type: "text/plain" });
        const privateUrl = URL.createObjectURL(privateBlob);
        const privateLink = document.createElement("a");
        privateLink.href = privateUrl;
        privateLink.download = "private_key.pem";
        privateLink.click();
        URL.revokeObjectURL(privateUrl);

        // Descargamos la clave pública
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
        console.log(e.target.result);
        setPrivateKey(e.target.result);
      };
      reader.readAsText(file);
    }
  };


  const handleUpload = () => {
    if (!selectedFile || !privateKey) {
      setMessage("Por favor selecciona un archivo y carga tu clave privada.");
      return;
    }

    postService.uploadFile(selectedFile, privateKey, signFile)
      .then((response) => {
        setMessage(`Archivo subido exitosamente: ${response.data.filename}`);
        fetchFiles(); // actualizar la lista automáticamente
      })
      .catch((error) => {
        console.error("Error al subir archivo:", error);
        setMessage("Error al subir archivo.");
      });
  };

  const handleDownload = (fileId) => {
    postService.downloadFile(fileId)
      .then((response) => {
        const { filename, content } = response.data;
        const blob = new Blob([atob(content)], { type: "application/octet-stream" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = filename;
        link.click();
        URL.revokeObjectURL(url);
      })
      .catch((error) => {
        console.error("Error al descargar archivo:", error);
        alert("Error al descargar archivo.");
      });
  };

  const handleVerify = () => {
    if (!fileToVerify || !ownerEmail) {
      setVerifyResult("Por favor selecciona un archivo y escribe el correo del propietario.");
      return;
    }
  
    postService.verifyFile(fileToVerify, ownerEmail)
      .then((response) => {
        setVerifyResult(response.data.message);
      })
      .catch((error) => {
        console.error("Error al verificar archivo:", error);
        if (error.response?.data?.error) {
          setVerifyResult("Error: " + error.response.data.error);
        } else {
          setVerifyResult("Error al verificar archivo.");
        }
      });
  };
  

  return (
    <div className="container text-center mt-5">
      {currentUser && (
        <>
          <h1 className="display-4 mb-4">Bienvenido</h1>
        {/* elegir el algoritmo */}
        <div className="mb-3">
            <label className="me-2">Elige el algoritmo:</label>
            <input
              type="radio"
              id="rsa"
              name="algorithm"
              value="rsa"
              checked={algorithm === "rsa"}
              onChange={(e) => setAlgorithm(e.target.value)}
            />
            <label htmlFor="rsa" className="me-3 ms-1">RSA</label>

            <input
              type="radio"
              id="ecc"
              name="algorithm"
              value="ecc"
              checked={algorithm === "ecc"}
              onChange={(e) => setAlgorithm(e.target.value)}
            />
            <label htmlFor="ecc" className="ms-1">ECC</label>
          </div>


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

      <h3 className="mt-5">Archivos</h3>
      <table className="table table-bordered mt-3">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Acción</th>
          </tr>
        </thead>
        <tbody>
          {privatePosts.map((post) => (
            <tr key={post.id}>
              <td>{post.filename} {post.is_signed ? "(Firmado)" : ""}</td>
              <td>
                <button
                  className="btn btn-outline-primary btn-sm"
                  onClick={() => handleDownload(post.id)}
                >
                  Descargar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <h3 className="mt-5">Verificar</h3>
        <p>Sube un archivo y el correo del propietario para verificar su autenticidad.</p>

        <div className="mb-3">
          <input
            type="file"
            className="form-control"
            onChange={(e) => setFileToVerify(e.target.files[0])}
          />
        </div>

        <div className="mb-3">
          <input
            type="email"
            placeholder="Correo del propietario"
            className="form-control"
            value={ownerEmail}
            onChange={(e) => setOwnerEmail(e.target.value)}
          />
        </div>

        <button className="btn btn-info" onClick={handleVerify}>
          Verificar
        </button>

        {verifyResult && (
          <div className="alert alert-warning mt-3">{verifyResult}</div>
        )}

    </div>
  );
};

export default Home;
