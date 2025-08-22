from flask import Flask, render_template, url_for

app = Flask(__name__)

# Home page
@app.route('/')
def index():
    services = [
        {"title": "Vaccination", "description": "Have your pets vaccinated at home.", "image": "imgs1.png", "link": "#"},
        {"title": "General Treatment", "description": "Experienced veterinarians will treat your pet right at your doorstep.", "image": "imgs2.jpg", "link": "#"},
        {"title": "Deworming", "description": "Fecal analysis and medication for parasite-free pets.", "image": "imgs3.jpg", "link": "#"},
        {"title": "Grooming", "description": "Bath, trim, and style your pet at home.", "image": "imgs4.jpg", "link": "#"},
        {"title": "Nail Trimming", "description": "Carefully trim your pet's nails.", "image": "nail.jpeg", "link": "#"},
        {"title": "Dental Care", "description": "Dental checkups and cleaning.", "image": "imgs6.jpg", "link": "#"},
        {"title": "Pet X-Ray", "description": "Advanced mobile X-ray service at home.", "image": "imgs7.jpg", "link": "#"},
        {"title": "Emergency Care", "description": "Quick response emergency services.", "image": "imgs8.jpg", "link": "#"},
        {"title": "Nutrition Guidance", "description": "Custom diet plans for your pet.", "image": "imgs9.jpg", "link": "#"}
    ]
    return render_template('index.html', services=services)
# 9 blog posts data
blogs = [
    {
        "title": "10 Essential Puppy Proofing Tips",
        "image": "images/puppy.jpeg",
        "excerpt": "Create a safe and friendly environment for your new best friend...",
        "link": "#"
    },
    {
        "title": "How to Take Care of Your Puppy and Feed Them",
        "image": "images/Maltese Dog 1.png",
        "excerpt": "The first week of the puppies' lives is the most critical to their survival...",
        "link": "#"
    },
    {
        "title": "Why Regular Veterinary Checkups are Important",
        "image": "images/img2.jpg",
        "excerpt": "Routine vet visits ensure your pet’s long-term health and well-being...",
        "link": "#"
    },
    {
        "title": "The Ultimate Pet Nutrition Guide",
        "image": "images/img4.jpg",
        "excerpt": "Learn how to provide a balanced diet for your pet to keep them healthy...",
        "link": "#"
    },
    {
        "title": "Top 5 Dog Training Tips for Beginners",
        "image": "images/img5.jpg",
        "excerpt": "Training your dog doesn’t have to be stressful. Follow these expert tips...",
        "link": "#"
    },
    {
        "title": "Essential Tips for Keeping Your Cat Happy",
        "image": "images/img10.jpg",
        "excerpt": "Cats require specific care and attention. Learn the best ways to care for them...",
        "link": "#"
    },
    {
        "title": "Caring for Senior Pets: What You Need to Know",
        "image": "images/img6.jpg",
        "excerpt": "Older pets need special care. Here are tips to keep them comfortable...",
        "link": "#"
    },
    {
        "title": "Choosing the Right Dog Breed for Your Lifestyle",
        "image": "images/img8.jpg",
        "excerpt": "Discover which dog breed suits your lifestyle the best...",
        "link": "#"
    },
    {
        "title": "How to Handle Pet Emergencies",
        "image": "images/img11.jpg",
        "excerpt": "Knowing how to act in an emergency can save your pet’s life...",
        "link": "#"
    }
]


# Gallery page
@app.route('/gallery')
def gallery():
    # Images are named gall1.jpeg -> gall20.jpeg
    return render_template('gallery.html')

# Blogs page
@app.route('/blogs')
def blogs():
    # You can pass blog posts as a list of dicts if needed
    return render_template('blogs.html')

# Services page
@app.route('/services')
def services():
    return render_template('services.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
