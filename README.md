<!--
PROJECT NAME
-->

# LABORATORIO 4 - CIFRADOS 2025  
<a id="readme-top"></a>

<!--
PROJECT DESCRIPTION
-->
## 📜 Descripción

El sistema permite a los usuarios registrarse y autenticarse mediante JSON Web Tokens (JWT), generar llaves públicas y privadas (ECC o RSA), firmar archivos digitalmente, verificar firmas, y validar la integridad de archivos con SHA-256.


---

## ✨ Características

- Registro seguro con hashing (SHA-256)
- Autenticación mediante JWT con expiración de 1 hora
- Generación de claves asimétricas (ECC / RSA)
- Firma y verificación de archivos digitalmente
- Validación de integridad con SHA-256
- Descarga de archivos cifrados y verificación de firma
- Gestión de archivos del usuario y de otros usuarios

---

## 🧩 Arquitectura General

- **Frontend:** React + HTML + CSS + JS
- **Backend:** Python + Flask
- **Criptografía:** PyCryptodome
- **Autenticación:** JWT
- **Hashing:** SHA-256
- **Firma Digital:** ECC / RSA

---

## 📐 Análisis y Diseño

### 🎯 Objetivos

Desarrollar una aplicación segura que permita:

- Registro e inicio de sesión usando JWT
- Hashing de contraseñas con SHA-256
- Firma digital con ECC o RSA
- Validación de archivos con SHA-256
- Acceso a archivos firmados y validados
- Confidencialidad mediante cifrado asimétrico

### 🔍 Alcance del Proyecto

- Registro/Login usando email y contraseña (hash protegida)
- Generación de llaves ECC/RSA tras iniciar sesión
- Subida de archivos con o sin firma digital
- Visualización y descarga de archivos
- Validación de firma y verificación de hash antes de descargar

### 👤 Usuarios Objetivo

- Cualquier persona que necesite firmar y compartir archivos con énfasis en seguridad, integridad y autenticidad.

---

## 📂 Estructura del Proyecto (En desarrollo)

<details>
  <summary>Descripción Provisional</summary>

- **frontend/** (React)
  - **components/**: Componentes reutilizables
  - **pages/**: Login, Registro, Home
  - **services/**: Peticiones API
- **backend/** (Flask)
  - **routes/**: Endpoints REST
  - **crypto/**: Lógica de firma y hash
  - **models/**: Manejo de usuarios y archivos
  - **auth/**: JWT y validación
</details>

<p align="right">(<a href="#readme-top">Ir al inicio</a>)</p>

---

## 📡 Endpoints Planeados

| Endpoint                   | Método | Descripción |
|---------------------------|--------|-------------|
| `/login`                  | POST   | Iniciar sesión con JWT |
| `/register`               | POST   | Crear usuario con contraseña hasheada |
| `/archivos`               | GET    | Listar archivos disponibles |
| `/archivos/{id}/descargar`| GET    | Descargar archivo y su llave pública |
| `/guardar`                | POST   | Guardar archivo con o sin firma |
| `/verificar`              | POST   | Verificar la firma digital del archivo |

---

## 📦 Dependencias Planeadas

* [![Node][Node.js]][Node-url]
* [![React][React.js]][React-url]
* [![Python][Python]][Python-url]
* [![Flask][Flask]][Flask-url]
* [![PyCryptodome][PyCryptodome]][PyCrypto-url]
* [![JWT][JWT]][JWT-url]

<p align="right">(<a href="#readme-top">Ir al inicio</a>)</p>

## ⚙️ Instrucciones de ejecución

### Frontend
1. Instalar dependencias:
```
npm install
```
2. Ejecutar proyecto (debe estar dentro del directorio /frontend)
```
npm run start
```

### Backend
1. Instalar dependencias (debe estar dentro del directorio /backend):
```
pip install -r requirements.txt
```
2. Ejecutar proyecto (debe estar dentro del directorio raíz)
```
python -m backend.run
```

## 🛡️ Seguridad

- 🔐 Contraseñas hasheadas con SHA-256
- 🧾 JWT con expiración de 1 hora
- 🔏 Firma digital con clave privada ECC/RSA
- ✅ Validación con clave pública antes de aceptar archivo
- 📎 Hash SHA-256 para verificar integridad

---

## 👥 Contribuciones

Si deseas contribuir al proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Haz tus cambios y haz commit (`git commit -m 'Añadir funcionalidad'`).
4. Sube la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

---

## 🧑‍💻 Developer

<a href="https://github.com/locano">
  <img width='75' src="https://avatars.githubusercontent.com/u/16949087?v=4" alt="Ludwing Cano" />
</a>

* [![Linkedin][Linkedin]][Linkedin-lud]
* [![GitHub][GitHub]][GitHub-lud]

---

## 📞 Contacto

* [![Instagram][Instagram]][Instagram-url]
* [![Website][Website]][Website-url]

<p align="right">(<a href="#readme-top">Ir al inicio</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[Node.js]: https://img.shields.io/badge/Node.js-339933?style=flat&logo=node.js&logoColor=white
[Node-url]: https://nodejs.org/en/
[React.js]: https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Python]: https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Flask]: https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/
[JWT]: https://img.shields.io/badge/JWT-black?style=flat&logo=JSON%20web%20tokens
[JWT-url]: https://jwt.io/
[PyCryptodome]: https://img.shields.io/badge/PyCryptodome-FFD43B?style=flat&logo=python&logoColor=black
[PyCrypto-url]: https://www.pycryptodome.org/
[Instagram]: https://img.shields.io/badge/Instagram-E4405F?style=flat&logo=instagram&logoColor=white
[Instagram-url]: https://www.instagram.com/ludwing238/
[Website]: https://img.shields.io/website?url=https://lc2tech.com/
[Website-url]: https://lc2tech.com/
[Linkedin]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[Linkedin-lud]: https://www.linkedin.com/in/ludwing-cano238
[GitHub]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white
[GitHub-lud]: https://github.com/locano




  
