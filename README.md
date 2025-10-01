🐾 Pet Hospital Management System

A Flask-based web application designed to manage pet hospital operations. It helps admins, doctors, and pet owners streamline appointments, maintain medical records, and improve communication.

📌 Features

👨‍⚕️ Admin Dashboard

Manage doctors, staff, and pet owners.

View and respond to appointment requests.

Track hospital activities and records.

🐶 Pet Owner Portal

Register pets and owner details.

Book and manage appointments.

View medical history and prescriptions.

💊 Doctor Dashboard

Manage appointments.

Update medical history and treatment notes.

View pet details and history.

📩 Messaging System

Secure communication between doctors, admins, and pet owners.

🔒 Authentication

Secure login system with hashed passwords.

Admin-only access to sensitive data.

🛠️ Tech Stack

Backend: Python, Flask

Frontend: HTML, Tailwind CSS (or Bootstrap)

Database: MySQL / SQLite

Authentication: Flask-Login / Session Management

Deployment: Gunicorn + Nginx (Linux server)

⚙️ Installation

Clone the repository

git clone https://github.com/yourusername/pet-hospital.git
cd pet-hospital


Create a virtual environment

python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)


Install dependencies

pip install -r requirements.txt


Setup database

Update database credentials in config.py.

Run migrations or create tables manually.

Start the application

flask run


Open in browser:

http://127.0.0.1:5000/

📂 Project Structure
pet-hospital/
│── app.py              # Main Flask app
│── config.py           # Configuration file
│── models.py           # Database models
│── static/             # CSS, JS, Images
│── templates/          # HTML templates
│── requirements.txt    # Dependencies
│── README.md           # Project documentation

🚀 Deployment

Use Gunicorn + Nginx on a Linux server for production.

Alternatively, deploy on Heroku, Render, or PythonAnywhere.

📌 Future Enhancements

🧾 Invoice/Billing system

📱 Mobile app for pet owners

🐕 Pet vaccination reminders via email/SMS

📊 Advanced reports for admins

🤝 Contributing

Contributions are welcome!

Fork the repo

Create a new branch

Commit changes

Submit a Pull Request

📜 License

This project is licensed under the MIT License – feel free to use and modify.
