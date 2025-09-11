# StudySphere

## Getting Started

### Prerequisites
Ensure you have the following installed:
- Docker & Docker Compose

### Clone the Repository
```bash
git clone https://github.com/yourusername/StudySphere.git
cd StudySphere/
```

### Setup Environment Variables
Create a `.env` file in the root directory and add the following variables:
```
DB_NAME=StudySphere_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=postgres_db
DB_PORT=5432
SECRET_KEY=your_SecretKey
```

### Running the Project with Docker
1. **Build & Start Containers**
```bash
docker-compose up --build
```

2. **Run Database Migrations**
```bash
docker exec -it django_app python manage.py migrate
```

3. **Create a Superuser**
```bash
docker exec -it django_app python manage.py createsuperuser
```
Follow the prompt to set up an admin account.

4. **Access the Application**
- **Django Admin Panel:** `http://localhost:8000/admin/`
- **API Endpoints:** `http://localhost:8000/api/`

### Stopping the Application
To stop and remove all containers, run:
```bash
docker-compose down
```

### Running Without Docker
If you prefer running the project locally without Docker:
1. **Create a Virtual Environment & Install Dependencies**
```bash
python -m venv env
source env\Scripts\activate
pip install -r requirements.txt
```
2. **Run Migrations & Start Server**
```bash
python manage.py migrate
python manage.py runserver
```

---

Happy coding! 🚀
