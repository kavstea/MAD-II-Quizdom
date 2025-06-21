# Quizdom-V2
A Flask + VueJS-based full-stack quiz management system. It introduces new features like exporting results, daily and monthly scheduled reminders, and support for both single and multiple quiz attempts, building on the original functionalities.

**Grade:**

**Live Link (demo/testing only):**

**[Quizdom-V2](https://quizdom-v2.onrender.com/)** 

(For best display on mobile: desktop view + landscape mode.)


---

## **Project Structure**
```
PROJECT_MAD2/
│
├── backend/
│   ├── __pycache__/
│   ├── api.py
│   ├── config.py
│   ├── models.py
│   ├── task.py
│   └── worker.py
│
├── frontend/
│   ├── .vscode/
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── router/
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── jsconfig.json
│   ├── package-lock.json
│   ├── package.json
│   ├── README.md
│   └── vite.config.js
│
├── instance/
│
├── reports/
│
├── templates/
│   └── report.html
│
├── .gitignore
├── app.py
├── celerybeat-schedule
├── readme.md
└── requirements.txt
```
---

## **Setup Instructions**

### **1. Backend (Flask API)**
#### a. (Recommended) Create and activate a virtual environment
#### b. Install Python dependencies
```
cd backend
pip install -r ../requirements.txt
```
#### c. Run the Flask server
From the project root
```
python app.py
```
- The API will be available at `http://localhost:5000/`.


#### d. (Optional) Celery & Redis for background tasks
- Make sure Redis is running (default: `localhost:6379`)
- Start Celery worker:
```
celery -A app.celery worker --loglevel=info

celery -A app.celery beat --loglevel=info

mailhog
```
---

### **2. Frontend (Vue.js SPA)**

#### a. Install Node.js dependencies
```
cd frontend
npm install
```

#### b. Run the Vue development server
```
npm run dev
```
- The app will be available at `http://localhost:5173/` (or as shown in your terminal).

---

### **3. API Documentation**

- The REST API is fully documented in `api.yaml` (OpenAPI 3.0 format).
- You can view and test the API using [Swagger Editor](https://editor.swagger.io/):
  - Open `api.yaml` in Swagger Editor for interactive docs.

---

### **4. Default Admin Login**

- Username: `admin`
- Password: `admin123`

---

### **5. Notes**

- CORS is enabled for frontend-backend communication.
- All environment/config files are in `backend/config.py`.
- The database will auto-create tables and a default admin user on first run.
- For email features, Mailhog is used for local SMTP testing.

---

### **6. Troubleshooting**

- If you get module errors, ensure you’re in the right folder and have installed all dependencies.
- If you change models, delete the old SQLite DB and let Flask re-create it.
- For background tasks, ensure Redis and Celery are both running.

---

## **Backend Overview**

- **app.py**: Entry point that creates the Flask app, initializes SQLAlchemy, JWT, CORS, cache, and Celery. Registers all API endpoints.
- **backend/api.py**: Contains all RESTful API resources (login, signup, CRUD for subjects/chapters/quizzes/questions, quiz attempt, stats, export, user management) using Flask-RESTful.
- **backend/models.py**: SQLAlchemy models for User, Subject, Chapter, Quiz, Question, and Score, with relationships and constraints.
- **backend/task.py**: Celery tasks for background jobs (e.g., exporting scores, sending emails).
- **backend/worker.py**: Celery worker initialization and configuration.
- **backend/config.py**: Configuration for Flask, database, JWT, caching, and Celery beat schedule.

---

## **Frontend Overview**

- **frontend/src/components/**: All Vue components for user and admin dashboards, quiz pages, scorecards, statistics (charts), login/signup, etc.
- **frontend/src/router/**: Vue Router configuration for SPA navigation.
- **frontend/src/App.vue** and **main.js**: Main entry point and root Vue component.
- **frontend/public/** and **assets/**: Static files, images, and icons.
- **frontend/vite.config.js**: Vite build tool configuration for fast development.

<div align="center">
  <em>---x---</em>
</div>  
