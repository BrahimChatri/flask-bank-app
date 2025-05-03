# 💸 Flask Bank App

A simple bank management system built with Flask and file-based data storage.  
The goal of this project is to learn and implement core backend concepts like authentication, CRUD operations, and data persistence — without using a database.

---

## 🚀 Features

- User Registration & Login
- Session-based Authentication
- Deposit & Withdraw Funds
- Transfer Between Users
- View Transaction History
- File-based Data Storage (JSON or similar)
- Modular Code Structure with Blueprints
- Simple and Clean HTML Templates

---

## 📁 Project Structure

```
bank_app/
│
├── api/                    # api folder to have api routes
|   ├── __init__.py
|   ├── api.py              # views for api routes
|
├── views/                  # Blueprint routes (e.g., banking, auth)
│   ├── __init__.py         # Register blueprints
│   ├── auth.py             # Auth-related routes
│   └── banking.py          # Banking operations
│
├── templates/              # HTML templates
│   ├── layout.html         # Base template
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── transfer.html
│   └── history.html
│
├── utils/                  # Helper modules
│   ├── storage.py          # File-based read/write logic
│   └── auth.py             # Password hashing & verification
│
├── static/                 # CSS, JS, images (if needed)
├── app.py                  # Main entry point to run the Flask app
└── README.md               # This file
```

---

## 🧠 Goals of This Project

- Practice authentication and session handling.
- Understand file-based data persistence.
- Organize a Flask project using blueprints.
- Build a real-world-like application step by step.
- Develop problem-solving and debugging skills.

---

## 📌 Requirements

- Python 3.x
- Flask
- Any other standard libraries (like `uuid`, `hashlib`, `json`)

---

## 🏃‍♂️ Running the App

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/BrahimChatri/flask-bank-app.git
cd flask-bank-app
```

### 2️⃣ Install Dependencies  
Ensure you have Python installed, then run:  
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Flask Server  
```bash
python app.py
```
Then, open **http://127.0.0.1:5000** in your browser.
---

## 💡 Notes

This is a learning-focused project. It doesn't use a database — everything is stored in simple JSON files.  
You’re encouraged to improve upon it later by adding database support, proper validation, better UI, and more advanced security.

---

## 📚 License

This project is for educational purposes. Use it to learn, break it, fix it, and improve it!
```

