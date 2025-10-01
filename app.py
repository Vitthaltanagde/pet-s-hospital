from os import abort
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'f62164cbb144fe8396e3bf51742cba41e82e7fa235394e50ff5166e292e994c6'  # Change this in production

# Home page
UPLOAD_FOLDER = "static/gallery"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Make sure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Vitthal@123",
    "database": "mrigaayuvets",
    "auth_plugin": "mysql_native_password"
}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_admin_context():
    """Get common admin context data"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get basic stats
        cursor.execute("SELECT COUNT(*) as count FROM gallery")
        total_images = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM appointments")
        total_appointments = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM appointments WHERE status = 'pending'")
        pending_appointments = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM contact_messages WHERE status = 'unread'")
        unread_messages = cursor.fetchone()['count']
        
        cursor.close()
        conn.close()
        
        return {
            'admin_username': session.get('admin_username', 'Admin'),
            'basic_stats': {
                'total_images': total_images,
                'total_appointments': total_appointments,
                'pending_appointments': pending_appointments,
                'unread_messages': unread_messages
            }
        }
    except:
        return {
            'admin_username': session.get('admin_username', 'Admin'),
            'basic_stats': {
                'total_images': 0,
                'total_appointments': 0,
                'pending_appointments': 0,
                'unread_messages': 0
            }
        }

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please login to access admin panel', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Database initialization function
def init_admin_database():
    """Initialize admin tables in the database"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Create admins table
        create_admin_table = """
        CREATE TABLE IF NOT EXISTS admins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            email VARCHAR(100),
            full_name VARCHAR(100),
            role VARCHAR(50) DEFAULT 'admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP NULL,
            is_active BOOLEAN DEFAULT TRUE
        )
        """
        
        # Create admin activity log
        create_admin_activity = """
        CREATE TABLE IF NOT EXISTS admin_activity (
            id INT AUTO_INCREMENT PRIMARY KEY,
            admin_id INT,
            activity VARCHAR(255),
            description TEXT,
            ip_address VARCHAR(45),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (admin_id) REFERENCES admins(id)
        )
        """
        
        # Create appointments table if not exists
        create_appointments_table = """
        CREATE TABLE IF NOT EXISTS appointments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            pet_name VARCHAR(100),
            service VARCHAR(100),
            preferred_date DATE,
            preferred_time TIME,
            message TEXT,
            status ENUM('pending', 'confirmed', 'completed', 'cancelled') DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Create contact messages table
        create_contact_table = """
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            subject VARCHAR(200),
            message TEXT,
            status ENUM('unread', 'read', 'replied') DEFAULT 'unread',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Create gallery table
        create_gallery_table = """
        CREATE TABLE IF NOT EXISTS gallery (
            id INT AUTO_INCREMENT PRIMARY KEY,
            image_path VARCHAR(255) NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        cursor.execute(create_admin_table)
        cursor.execute(create_admin_activity)
        cursor.execute(create_appointments_table)
        cursor.execute(create_contact_table)
        cursor.execute(create_gallery_table)
        
        # Check if default admin exists
        cursor.execute("SELECT COUNT(*) FROM admins WHERE username = 'admin'")
        if cursor.fetchone()[0] == 0:
            # Create default admin
            admin_password = generate_password_hash('admin123')
            cursor.execute(
                "INSERT INTO admins (username, password_hash, email, full_name, role) VALUES (%s, %s, %s, %s, %s)",
                ('admin', admin_password, 'admin@mrigaayuvets.com', 'System Administrator', 'super_admin')
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Admin database initialized successfully!")
        
    except Error as e:
        print(f"Error initializing admin database: {e}")

# Your existing data dictionaries
blogs_data = {
   "puppy_proofing": {
        "id": "puppy_proofing",
        "title": "10 Essential Puppy Proofing Tips from SKvets",
        "image": "images/puppy.jpeg",
        "excerpt": "Create a safe and friendly environment for your new best friend...",
        "file": "blogs/puppy_proofing.html"
    },
    "puppy_care":{ 
        "title": "How to take care of your Puppy and feed them?",
        "image": "images/Maltese Dog 1.png",
        "excerpt": "The first week of the puppies' lives is the most critical to their survival...",
        "file": "blogs/puppy_care.html"
    },
    "vet_checkups":{
        "title": "Why Regular Veterinary Checkups are Important",
        "image": "images/img2.jpg",
        "excerpt": "Routine vet visits ensure your pet's long-term health and well-being...",
        "file": "blogs/vet_checkups.html"
    },
    "pet_nutrition":{
        "title": "The Ultimate Pet Nutrition Guide",
        "image": "images/img4.jpg",
        "excerpt": "Learn how to provide a balanced diet for your pet to keep them healthy...",
        "file": "blogs/pet_nutrition.html"
    },
    "dog_training":{
        "title": "Top 5 Dog Training Tips for Beginners",
        "image": "images/img5.jpg",
        "excerpt": "Training your dog doesn't have to be stressful. Follow these expert tips...",
        "file": "blogs/dog_training.html"
    },
    "cat_care":{
        "title": "Essential Tips for Keeping Your Cat Happy",
        "image": "images/img10.jpg",
        "excerpt": "Cats require specific care and attention. Learn the best ways to care for them...",
        "file": "blogs/cat_care.html"
    },
    "senior_pet_care":{
        "title": "Caring for Senior Pets: What You Need to Know",
        "image": "images/img6.jpg",
        "excerpt": "Older pets need special care. Here are tips to keep them comfortable...",
        "file": "blogs/senior_pet_care.html"
    },
    "dog_breeds":{
        "title": "Choosing the Right Dog Breed for Your Lifestyle",
        "image": "images/img8.jpg",
        "excerpt": "Discover which dog breed suits your lifestyle the best...",
        "file": "blogs/dog_breeds.html"
    },
    "pet_emergencies":{
        "title": "How to Handle Pet Emergencies",
        "image": "images/img11.jpg",
        "excerpt": "Knowing how to act in an emergency can save your pet's life...",
        "file": "blogs/pet_emergencies.html"
    }
}

services_data = {
    "vaccination": {
        "title": "Pet Vaccination Services",
        "image": "imgs1.png",
        "description": "Comprehensive vaccination services for your pets at home",
        "file": "services/vaccination.html"
    },
    "general_treatment": {
        "title": "General Pet Treatment",
        "image": "imgs2.jpg",
        "description": "Comprehensive general treatment services for all your pet's health needs",
        "file": "services/general_treatment.html"
    },
    "deworming": {
        "title": "Pet Deworming Services",
        "image": "imgs3.jpg",
        "description": "Professional deworming services with fecal analysis",
        "file": "services/deworming.html"
    },
    "grooming": {
        "title": "Pet Grooming Services",
        "image": "imgs4.jpg",
        "description": "Professional grooming services in the comfort of your home",
        "file": "services/grooming.html"
    },
    "nail_trimming": {
        "title": "Professional Nail Trimming",
        "image": "nail.jpeg",
        "description": "Expert nail care to keep your pet comfortable and healthy",
        "file": "services/nail_trimming.html"
    },
    "dental_care": {
        "title": "Pet Dental Care",
        "image": "imgs6.jpg",
        "description": "Comprehensive dental health services for your pet",
        "file": "services/dental_care.html"
    },
    "pet_xray": {
        "title": "Mobile Pet X-Ray Services",
        "image": "imgs7.jpg",
        "description": "Advanced diagnostic imaging at your doorstep",
        "file": "services/pet_xray.html"
    },
    "emergency_care": {
        "title": "24/7 Emergency Pet Care",
        "image": "imgs8.jpg",
        "description": "Immediate veterinary response for urgent situations",
        "file": "services/emergency_care.html"
    },
    "nutrition_guidance": {
        "title": "Pet Nutrition Consultation",
        "image": "imgs9.jpg",
        "description": "Personalized nutrition plans for optimal pet health",
        "file": "services/nutrition_guidance.html"
    }
}

# ===========================================
# PUBLIC ROUTES
# ===========================================

@app.route('/')
def index():
    services = []
    for service_id, data in services_data.items():
        services.append({
            "title": data["title"],
            "description": data["description"],
            "image": data["image"],
            "link": url_for('service_detail', service_id=service_id)
        })
    return render_template('index.html', services=services)

@app.route('/contact_form_submit', methods=['POST'])
def contact_form_submit():
    """Handle contact form submission from homepage"""
    if request.method == 'POST':
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            
            # Map homepage form fields to database fields
            name = request.form.get('full_name', '') or request.form.get('name', '')
            email = request.form.get('email', '')
            subject = request.form.get('subject', '')
            message = request.form.get('message', '')
            
            cursor.execute("""
                INSERT INTO contact_messages (name, email, subject, message)
                VALUES (%s, %s, %s, %s)
            """, (name, email, subject, message))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Message sent successfully! We will get back to you soon.', 'success')
            return redirect(url_for('index') + '#contact')
            
        except Error as e:
            flash(f'Error sending message: {e}', 'error')
            return redirect(url_for('index') + '#contact')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        # Handle appointment form submission
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            
            # Insert appointment data
            cursor.execute("""
                INSERT INTO appointments (name, email, phone, pet_name, service, preferred_date, preferred_time, message)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                request.form['name'],
                request.form['email'],
                request.form['phone'],
                request.form.get('pet_name', ''),
                request.form.get('service', ''),
                request.form.get('preferred_date') if request.form.get('preferred_date') else None,
                request.form.get('preferred_time') if request.form.get('preferred_time') else None,
                request.form.get('message', '')
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            # Check which action was taken
            action = request.form.get('action', 'database')
            
            if action == 'database':
                flash('Appointment request submitted successfully! We will contact you soon.', 'success')
            
            return redirect(url_for('appointment'))
            
        except Error as e:
            flash(f'Error submitting appointment: {e}', 'error')
    
    return render_template('appointment.html')

@app.route("/gallery")
def gallery():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gallery ORDER BY uploaded_at DESC")
    images = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("gallery.html", images=images)

@app.route('/blogs')
def blogs():
    return render_template('blogs.html', blogs=blogs_data)

@app.route('/blog/<blog_id>')
def blog_detail(blog_id):
    blog = blogs_data.get(blog_id)
    if not blog:
        abort(404)
    return render_template(blog["file"], blog=blog)

@app.route('/services')
def services():
    return render_template('services.html', services=services_data)

@app.route('/service/<service_id>')
def service_detail(service_id):
    service = services_data.get(service_id)
    if not service:
        abort(404)
    return render_template(service["file"], service=service)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            
            # Handle both homepage and contact page form submissions
            name = request.form.get('name') or request.form.get('full_name', '')
            email = request.form.get('email', '')
            subject = request.form.get('subject', '')
            message = request.form.get('message', '')
            
            # Insert contact message
            cursor.execute("""
                INSERT INTO contact_messages (name, email, subject, message)
                VALUES (%s, %s, %s, %s)
            """, (name, email, subject, message))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            # Check which action was taken
            action = request.form.get('action', 'database')
            
            if action == 'database':
                flash('Message sent successfully! We will get back to you soon.', 'success')
            
            # Check if request came from homepage (has full_name field) or contact page
            if request.form.get('full_name'):
                return redirect(url_for('index') + '#contact')
            else:
                return redirect(url_for('contact'))
            
        except Error as e:
            flash(f'Error sending message: {e}', 'error')
            # Redirect based on form source
            if request.form.get('full_name'):
                return redirect(url_for('index') + '#contact')
            else:
                return redirect(url_for('contact'))
    
    return render_template('contact.html')

# ===========================================
# ADMIN ROUTES
# ===========================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admins WHERE username = %s AND is_active = TRUE", (username,))
            admin = cursor.fetchone()
            
            if admin and check_password_hash(admin['password_hash'], password):
                session['admin_id'] = admin['id']
                session['admin_username'] = admin['username']
                session['admin_role'] = admin['role']
                
                # Update last login
                cursor.execute("UPDATE admins SET last_login = %s WHERE id = %s", (datetime.now(), admin['id']))
                
                # Log login activity
                cursor.execute(
                    "INSERT INTO admin_activity (admin_id, activity, description, ip_address) VALUES (%s, %s, %s, %s)",
                    (admin['id'], 'Admin Login', f'Admin {username} logged in', request.remote_addr)
                )
                
                conn.commit()
                flash('Login successful!', 'success')
                cursor.close()
                conn.close()
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password', 'error')
                cursor.close()
                conn.close()
                
        except Error as e:
            flash(f'Database connection error: {e}', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@app.route('/logout')
def admin_logout():
    if 'admin_id' in session:
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO admin_activity (admin_id, activity, description, ip_address) VALUES (%s, %s, %s, %s)",
                (session['admin_id'], 'Admin Logout', f'Admin {session["admin_username"]} logged out', request.remote_addr)
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            print(f"Error logging logout activity: {e}")
    
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get dashboard statistics
        stats = {}
        
        # Total gallery images
        cursor.execute("SELECT COUNT(*) as count FROM gallery")
        stats['total_images'] = cursor.fetchone()['count']
        
        # Total appointments
        cursor.execute("SELECT COUNT(*) as count FROM appointments")
        stats['total_appointments'] = cursor.fetchone()['count']
        
        # Pending appointments
        cursor.execute("SELECT COUNT(*) as count FROM appointments WHERE status = 'pending'")
        stats['pending_appointments'] = cursor.fetchone()['count']
        
        # Unread messages
        cursor.execute("SELECT COUNT(*) as count FROM contact_messages WHERE status = 'unread'")
        stats['unread_messages'] = cursor.fetchone()['count']
        
        # Recent activities
        cursor.execute("""
            SELECT aa.*, a.username 
            FROM admin_activity aa 
            JOIN admins a ON aa.admin_id = a.id 
            ORDER BY aa.created_at DESC 
            LIMIT 10
        """)
        activities = cursor.fetchall()
        
        # Recent appointments
        cursor.execute("""
            SELECT * FROM appointments 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        recent_appointments = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('admin/dashboard.html', 
                             stats=stats, 
                             activities=activities,
                             recent_appointments=recent_appointments,
                             admin_username=session['admin_username'])
        
    except Error as e:
        flash(f'Database error: {e}', 'error')
        return redirect(url_for('admin_login'))

# Gallery management (updated with admin protection)
@app.route("/admin/gallery")
@admin_required
def admin_gallery():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get all images
        cursor.execute("SELECT * FROM gallery ORDER BY uploaded_at DESC")
        images = cursor.fetchall()
        
        # Get gallery statistics
        cursor.execute("SELECT COUNT(*) as total FROM gallery")
        total_images = cursor.fetchone()['total']
        
        # Get recent uploads (last 7 days)
        cursor.execute("""
            SELECT COUNT(*) as recent 
            FROM gallery 
            WHERE uploaded_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        """)
        recent_uploads = cursor.fetchone()['recent']
        
        # Prepare stats for template
        gallery_stats = {
            'total': total_images,
            'recent': recent_uploads
        }
        
        cursor.close()
        conn.close()
        
        return render_template("admin/gallery.html", 
                             images=images, 
                             stats=gallery_stats,
                             admin_username=session['admin_username'])
        
    except Error as e:
        flash(f'Database error: {e}', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route("/admin/upload", methods=["GET", "POST"])
@admin_required
def upload_image():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file selected", "error")
            return redirect(request.url)
        
        file = request.files["file"]
        if file.filename == "":
            flash("No file selected", "error")
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Save to MySQL
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO gallery (image_path) VALUES (%s)", (filename,))
            
            # Log activity
            cursor.execute(
                "INSERT INTO admin_activity (admin_id, activity, description, ip_address) VALUES (%s, %s, %s, %s)",
                (session['admin_id'], 'Image Upload', f'Uploaded image: {filename}', request.remote_addr)
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            flash("Image uploaded successfully!", "success")
            return redirect(url_for("admin_gallery"))
        else:
            flash("Invalid file type. Please upload PNG, JPG, JPEG, or GIF files.", "error")

    # Get admin context for GET request
    context = get_admin_context()
    return render_template("admin/upload.html", **context)

@app.route("/admin/delete/<int:image_id>", methods=["POST"])
@admin_required
def delete_image(image_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Get image filename from DB
    cursor.execute("SELECT image_path FROM gallery WHERE id = %s", (image_id,))
    image = cursor.fetchone()

    if image:
        filename = image["image_path"]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # Delete file from static/gallery
        if os.path.exists(filepath):
            os.remove(filepath)

        # Delete record from DB
        cursor.execute("DELETE FROM gallery WHERE id = %s", (image_id,))
        
        # Log activity
        cursor.execute(
            "INSERT INTO admin_activity (admin_id, activity, description, ip_address) VALUES (%s, %s, %s, %s)",
            (session['admin_id'], 'Image Delete', f'Deleted image: {filename}', request.remote_addr)
        )
        
        conn.commit()
        flash("Image deleted successfully!", "success")
    else:
        flash("Image not found!", "error")

    cursor.close()
    conn.close()
    return redirect(url_for("admin_gallery"))

# Appointments management
@app.route('/admin/appointments')
@admin_required
def admin_appointments():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get all appointments
        cursor.execute("SELECT * FROM appointments ORDER BY created_at DESC")
        appointments = cursor.fetchall()
        
        # Get appointment statistics
        cursor.execute("SELECT COUNT(*) as total FROM appointments")
        total_appointments = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as pending FROM appointments WHERE status = 'pending'")
        pending_appointments = cursor.fetchone()['pending']
        
        cursor.execute("SELECT COUNT(*) as confirmed FROM appointments WHERE status = 'confirmed'")
        confirmed_appointments = cursor.fetchone()['confirmed']
        
        cursor.execute("SELECT COUNT(*) as completed FROM appointments WHERE status = 'completed'")
        completed_appointments = cursor.fetchone()['completed']
        
        cursor.execute("SELECT COUNT(*) as cancelled FROM appointments WHERE status = 'cancelled'")
        cancelled_appointments = cursor.fetchone()['cancelled']
        
        # Prepare stats for template
        appointment_stats = {
            'total': total_appointments,
            'pending': pending_appointments,
            'confirmed': confirmed_appointments,
            'completed': completed_appointments,
            'cancelled': cancelled_appointments
        }
        
        cursor.close()
        conn.close()
        
        return render_template('admin/appointments.html', 
                             appointments=appointments, 
                             stats=appointment_stats,
                             admin_username=session['admin_username'])
        
    except Error as e:
        flash(f'Database error: {e}', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/appointment/<int:appointment_id>/update', methods=['POST'])
@admin_required
def update_appointment_status(appointment_id):
    status = request.form.get('status')
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("UPDATE appointments SET status = %s WHERE id = %s", (status, appointment_id))
    
    # Log activity
    cursor.execute(
        "INSERT INTO admin_activity (admin_id, activity, description, ip_address) VALUES (%s, %s, %s, %s)",
        (session['admin_id'], 'Appointment Update', f'Updated appointment #{appointment_id} status to {status}', request.remote_addr)
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f'Appointment status updated to {status}!', 'success')
    return redirect(url_for('admin_appointments'))

# Contact messages management
@app.route('/admin/messages')
@admin_required
def admin_messages():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get all messages
        cursor.execute("SELECT * FROM contact_messages ORDER BY created_at DESC")
        messages = cursor.fetchall()
        
        # Get message statistics
        cursor.execute("SELECT COUNT(*) as total FROM contact_messages")
        total_messages = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as unread FROM contact_messages WHERE status = 'unread'")
        unread_messages = cursor.fetchone()['unread']
        
        cursor.execute("SELECT COUNT(*) as read FROM contact_messages WHERE status = 'read'")
        read_messages = cursor.fetchone()['read']
        
        cursor.execute("SELECT COUNT(*) as replied FROM contact_messages WHERE status = 'replied'")
        replied_messages = cursor.fetchone()['replied']
        
        # Prepare stats for template
        message_stats = {
            'total': total_messages,
            'unread': unread_messages,
            'read': read_messages,
            'replied': replied_messages
        }
        
        cursor.close()
        conn.close()
        
        return render_template('admin/messages.html', 
                             messages=messages, 
                             stats=message_stats,
                             admin_username=session['admin_username'])
        
    except Error as e:
        flash(f'Database error: {e}', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/message/<int:message_id>/mark_read', methods=['POST'])
@admin_required
def mark_message_read(message_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("UPDATE contact_messages SET status = 'read' WHERE id = %s", (message_id,))
    
    # Log activity
    cursor.execute(
        "INSERT INTO admin_activity (admin_id, activity, description, ip_address) VALUES (%s, %s, %s, %s)",
        (session['admin_id'], 'Message Read', f'Marked message #{message_id} as read', request.remote_addr)
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Message marked as read!', 'success')
    return redirect(url_for('admin_messages'))

# Route aliases for template compatibility
@app.route('/login')
def login():
    return redirect(url_for('admin_login'))

@app.route('/dashboard')
@admin_required
def dashboard():
    return redirect(url_for('admin_dashboard'))

@app.route('/appointments')
@admin_required  
def appointments():
    return redirect(url_for('admin_appointments'))

@app.route('/messages')
@admin_required
def messages():
    return redirect(url_for('admin_messages'))

if __name__ == "__main__":
    # Initialize admin database on startup
    init_admin_database()
    port = int(os.environ.get("PORT", 4000))
    app.run(host="0.0.0.0", port=port, debug=True)