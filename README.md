# Full-Stack Django Social Network Application (InstaApp)

A robust, enterprise-grade full-stack social networking application built using Python, Django, and the Django REST Framework (DRF). This project features a highly optimized relational database architecture, dynamic front-end interactions via AJAX, asynchronous-style event tracking for user notifications, a secure token-authenticated API layer, and a live production cloud deployment backed by PostgreSQL.

🚀 Live Application
Live Demo: http://18.60.44.93
(Note: As this is hosted on a free-tier AWS EC2 instance, please allow a moment for the initial connection).

🏗️ Infrastructure & Deployment Architecture
This application is deployed on bare-metal cloud infrastructure using a fully containerized, multi-service architecture to ensure production-grade security and scalability.

Cloud Provider: AWS EC2 (Ubuntu Linux)

Containerization: Docker & Docker Compose

Web Server / Reverse Proxy: Nginx

WSGI HTTP Server: Gunicorn

Backend Framework: Django (Python)

Database: PostgreSQL

Architecture Flow:

Client Requests hit the AWS EC2 public IP.

Nginx intercepts the traffic on Port 80, serves static files (CSS/JS) directly for high performance, and acts as a secure reverse proxy.

Gunicorn receives dynamic requests from Nginx and translates them for the Python environment.

Django processes the business logic and queries the isolated PostgreSQL database container via a secure internal Docker network.

---

## 🛠️ Technical Architecture & Core Features

### 1. Robust Core & Relational Database Design
* **Custom Registration & Profiling:** Unified workflow capturing standard credentials (`User`) alongside customized extended models (`Profile`), handling native file/image uploads securely using multi-part encryption logic.
* **Asymmetric Social Graph:** Implemented a self-referential, non-symmetrical Many-to-Many relationship model to seamlessly track asymmetric user connections (Followers/Following mechanics).
* **Dynamic Client-Side UI (AJAX):** Integrated vanilla JavaScript/jQuery asynchronous tracking to process post actions (likes/unlikes) instantly without forcing expensive browser page reloads.

### 2. Event-Driven Notification Engine
* **State Tracking Backend:** Uses an explicit database-backed transaction register to capture system-wide user events.
* **Contextual Triggers:** Instantly dispatches, modifies, or purges user notification objects across three distinct system matrices:
    1.  **Likes:** Tracks high-volume interactions while intentionally suppressing self-notifications.
    2.  **Comments:** Formats and displays micro-strings of user feedback strings dynamically.
    3.  **Follows:** Dispatches real-time identity mapping when social graph graphs change.

### 3. Enterprise-Grade Secured API Layer (DRF)
* **Decoupled Architecture:** Features a modular serialization engine (`ModelSerializer`) extracting application layer details into structured JSON schemas.
* **Token Authentication Workflow:** Enforces enterprise-level security by locking public routes behind a token authentication barrier. External client consumers must provide an `Authorization: Token <secret_key>` header validation token.
* **Postman Verified:** Thoroughly validated through multi-stage API integration tests verifying response states (`200 OK`, `401 Unauthorized`, `405 Method Not Allowed`).

### 4. Cloud DevOps & Production Pipeline
* **Database Modernization:** Migrated local storage setups effortlessly from developer SQLite engines to an enterprise-grade cloud **PostgreSQL** instance.
* **Static Asset Management:** Implemented **WhiteNoise** middleware configuration to compress and safely distribute system CSS/JS assets directly inside container environments.
* **Continuous Deployment (CI/CD):** Configured specialized shell configurations (`build.sh`) to automatically pull updates, manage packages (`requirements.txt`), execute production migrations, and initialize **Gunicorn WSGI** web worker servers automatically upon git pushes to Render.

---

## 🧰 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend Framework** | Python 3.12+ / Django 5.x |
| **API Architecture** | Django REST Framework (DRF) |
| **Database** | PostgreSQL (Production) / SQLite (Local Testing) |
| **WSGI HTTP Server** | Gunicorn |
| **Static Asset Management** | WhiteNoise Middleware |
| **Frontend Layout** | Tailwind CSS / HTML5 / JavaScript (AJAX / jQuery) |
| **Deployment Cloud** | Render Cloud Platform |

---

## 💾 Database Schema Overview

The application architecture utilizes optimized entity relations to scale data operations:

* **User (Django Built-in):** Handles authentication keys, names, and emails.
* **Profile:** Extended `OneToOne` user model managing profile pictures and a self-referential `ManyToManyField` mapping the followers' social graph topology.
* **Post:** Relational model mapping authors (`ForeignKey` -> User), images, captions, and an explicit tracking matrix (`ManyToManyField` -> User) to count and identify post likes efficiently.
* **Notification:** Central activity ledger tracking system-wide engagement types using structured choice mappings.

---