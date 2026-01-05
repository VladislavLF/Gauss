# Gauss
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) ![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)<br /><br />
Gauss is a comprehensive Django-based web application designed for mathematics exam preparation. The platform provides students with access to practice problems, theory materials, and exam variants to help prepare for standardized math exams. <br />

## Core Functionality
- Task Catalog - organized collection of math problems categorized by difficulty and topic.
- Exam Variants - complete practice exams with 18 tasks each.
- Theory Library - structured math theory by subject area.
- User Accounts - registration, authentication, and user profiles.
- Comment System - users can discuss and ask questions about specific tasks.

## Stack
### Backend
- Django 5.2 - Python web framework
- PostgreSQL - Primary database
- Redis - Caching and session management
- Gunicorn - WSGI HTTP server
### Frontend
- HTML5/CSS3 - Frontend markup and styling
- Django Templates - Server-side rendering
- JavaScript - Client-side interactivity
### Infrastructure
- Docker - Containerization
- Docker Compose - Multi-container orchestration
- Nginx - Web server and reverse proxy

## Quick start
### 1. Prerequisites
- Docker
- Git
- Python 3.12+ (for local development without Docker)
### 2. Installation and launch
#### 2.1. Clone the repository
`git clone <repository-url>`
`cd Gauss`
#### 2.2. Set up environment variables
`cp .env.production.example .env` or `cp .env.development.example .env`
#### 2.3. Launch the project
`docker-compose --env-file .env up --build`

## Site images
<img width="1860" height="939" alt="image" src="https://github.com/user-attachments/assets/9116bcc7-ea36-4ff3-b5d5-69ff1c965f85" /><br />
<img width="1855" height="932" alt="image" src="https://github.com/user-attachments/assets/d58d8d20-158c-4d00-a5c5-ba1d907afc2a" /><br />
<img width="1858" height="929" alt="image" src="https://github.com/user-attachments/assets/4c1bb949-8302-413a-b7a2-fcd78777fa37" /><br />
<img width="1859" height="934" alt="image" src="https://github.com/user-attachments/assets/90527be4-d000-4c0e-adbc-665d71492f8d" /><br />
<img width="1859" height="930" alt="image" src="https://github.com/user-attachments/assets/8351de28-d1b3-4673-890d-dd6a9b6ddc5c" /><br />
<img width="1862" height="930" alt="image" src="https://github.com/user-attachments/assets/27dbbc5c-7f1f-4423-8ec3-394cf5f6fd40" /><br />
<img width="1868" height="937" alt="image" src="https://github.com/user-attachments/assets/049011d4-6e69-423d-9b00-ee216a06e45b" />
