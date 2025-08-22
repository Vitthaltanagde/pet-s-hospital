🏥 Doctor Appointment Website

A modern, responsive Doctor Appointment Website built with Flask (Python), Tailwind CSS, and FontAwesome.
This project allows patients to quickly connect with doctors via WhatsApp, phone calls, or appointment booking forms.

✨ Features

📱 Responsive Design (Mobile + Desktop friendly)

📞 Direct Call Button (sticky bar on desktop, floating button on mobile)

💬 WhatsApp Appointment Booking with pre-filled message

🎨 Modern Tailwind UI with gradients, animations, and shadows

🔗 Navbar, Contact Page, About Page, and Layout Integration

🌐 LAN Access (Run on local Wi-Fi to test on any device)

🛠️ Tech Stack

Backend: Python (Flask)

Frontend: HTML5, Tailwind CSS, FontAwesome

Deployment Ready: Compatible with Gunicorn + Nginx (AWS / VPS hosting)

🚀 Getting Started
1️⃣ Clone the Repository
git clone https://github.com/yourusername/doctor-appointment-site.git
cd doctor-appointment-site

2️⃣ Install Dependencies
pip install -r requirements.txt


Example requirements.txt:

Flask
Flask-Mail

3️⃣ Run Locally
flask run


Visit:

http://127.0.0.1:5000

4️⃣ Run on Local Wi-Fi (LAN Testing)

To access from your mobile:

flask run --host=0.0.0.0 --port=5000
📸 Screenshots

🖥️ Desktop View → Navbar + Sticky Call Bar

📱 Mobile View → Floating WhatsApp & Call Buttons

🎨 Contact Page → Gradient Hero Section + Info

📦 Deployment
Using Gunicorn + Nginx (Linux server)
gunicorn -w 4 app:app -b 0.0.0.0:8000

👨‍⚕️ Author

Dr. Appointment Website developed by Your Name

📧 Contact: your@email.com
