# Flask CRUD Application with Authentication & CI/CD

This project is a **Flask-based CRUD web application** with **user authentication**, fully **Dockerized**, and integrated with a **CI/CD pipeline using GitHub Actions**.

It is designed as a **minor project** but follows **industry-standard DevOps practices**.

---

## 🚀 Features

- User Signup & Login (Authentication)
- CRUD Operations (Create, Read, Update, Delete)
- SQLite Database
- Clean and responsive UI (Bootstrap)
- Dockerized Application
- CI/CD using GitHub Actions
- Automatic Docker image build & push on every commit

---

## 🧱 Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **OS Support:** Linux, macOS (Intel & Apple Silicon), Windows

---

## 🖥️ Prerequisites

Make sure you have the following installed:

- **Python 3.9+**
- **Docker**
- **Git**
  
---

### Verify installations:
```bash
python --version
docker --version
git --version
```
⚙️ Installation & Setup (Local – Without Docker)

1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/flask-crud-app.git
cd flask-crud-app
```
2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
4️⃣ Run the Application
```bash
python app.py
```
🐳 Run Using Docker (Recommended)
1️⃣ Build Docker Image
```bash
docker build -t flask-crud-app .
```
2️⃣ Run Docker Container

macOS users should avoid port 5000 (often already in use)
```bash
docker run -p 5001:5000 flask-crud-app
```
